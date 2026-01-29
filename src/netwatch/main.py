import asyncio
import logging
from inspect import get_annotations
from types import get_original_bases
from typing import get_args

import apprise
from playwright.async_api import Browser, async_playwright

from netwatch.config import settings
from netwatch.database.connection import get_session
from netwatch.database.models import Post
from netwatch.provider.base import BaseProvider

logger = logging.getLogger(__name__)
apobj = apprise.Apprise()


def main():
    logging.basicConfig(level=logging.DEBUG)

    apobj.add(settings.notifications)  # type: ignore
    logger.info(f"Initialized {len(settings.notifications)} notification services")

    provider_cls_map = {}
    for provider_cls in BaseProvider.__subclasses__():
        base_provider = get_original_bases(provider_cls)[0]
        provider_args = get_args(base_provider)
        if not provider_args:
            logger.error(f"Could not determine source type for provider {provider_cls}")
            continue
        base_source = provider_args[0]
        annotations = get_annotations(base_source)
        source_provider_args = get_args(annotations.get("provider"))
        if not source_provider_args:
            logger.error(f"Could not determine provider for source {base_source}")
            continue
        provider = source_provider_args[0]
        provider_cls_map[provider] = provider_cls

    providers = []
    for source in settings.sources:
        provider_cls = provider_cls_map.get(source.provider)
        assert provider_cls is not None
        provider = provider_cls(source)
        providers.append(provider)

    logger.info(f"Initialized {len(providers)} providers")
    try:
        asyncio.run(poll(providers))
    except KeyboardInterrupt:
        pass


async def poll_provider(provider: BaseProvider, browser: Browser):
    with get_session() as session:
        try:
            async for post in provider.fetch(browser=browser):
                p = Post(**post.model_dump())
                new = session.get(Post, (p.provider, p.post_id, p.comment_id)) is None
                session.merge(p)
                session.commit()
                logger.info(f"Fetched post: {post.url}")
                if new:
                    body = f"{post.author}: {post.title}\n{post.content}\n[View Post]({post.url})"
                    if post.comment_id:
                        body = f"Reply {post.provider}:{post.post_id}:{post.comment_id}\n{body}"
                    else:
                        body = f"Post {post.provider}:{post.post_id}\n{body}"
                    await apobj.async_notify(
                        body=body,
                        title=post.title,
                        body_format=apprise.NotifyFormat.MARKDOWN,
                    )
        except:
            logger.exception(f"Error fetching posts from provider: {provider}")


async def poll(providers: list[BaseProvider]):
    while True:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            await asyncio.gather(
                *(poll_provider(provider, browser) for provider in providers)
            )
            await browser.close()
            await asyncio.sleep(600)
