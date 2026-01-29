import logging
from collections.abc import AsyncIterator
from typing import Literal
from urllib.parse import parse_qs, urlparse

from playwright.async_api import Browser, Locator

from netwatch.provider.base import BaseProvider, BaseSource, Post

logger = logging.getLogger(__name__)


class FacebookSource(BaseSource):
    provider: Literal["facebook"]
    page_id: str


class FacebookProvider(BaseProvider[FacebookSource]):
    async def fetch(self, *, browser: Browser, **_) -> AsyncIterator[Post]:
        page = await browser.new_page()

        logger.debug(f"Fetching Facebook page: {self.source.page_id}")
        await page.goto(f"https://www.facebook.com/groups/{self.source.page_id}")

        await page.evaluate("document.querySelector('div.__fb-light-mode').remove()")

        page.set_default_timeout(2000)

        articles = await page.locator('div[role="article"]').all()
        for article in articles:
            try:
                async for post in self._fetch_post(article):
                    yield post
            except Exception:
                logger.debug("Failed to parse post, skipping")

        await page.close()

    async def _fetch_post(self, article: Locator) -> AsyncIterator[Post]:
        profile_name = await article.locator(
            'div[data-ad-rendering-role="profile_name"]'
        ).first.inner_text()
        logger.debug(f"Found post by author: {profile_name}")
        created_at = article.locator('a[role="link"][aria-label]:not(:has(*))')
        post_url = await created_at.first.get_attribute("href")
        assert post_url
        post_id = urlparse(post_url).path.strip("/").split("/")[-1]
        content = await article.locator(
            'div[data-ad-rendering-role="story_message"]'
        ).first.inner_text()
        yield Post(
            provider="facebook",
            post_id=post_id,
            comment_id="",
            url=post_url,
            author=profile_name,
            title="",
            content=content,
        )
        for comment in await article.locator('div[role="article"]').all():
            try:
                yield await self._fetch_comment(post_id, comment)
            except Exception:
                logger.debug("Failed to parse comment, skipping")

    async def _fetch_comment(self, post_id: str, comment: Locator) -> Post:
        profile_name = await comment.locator('div[aria-hidden="false"]').inner_text()
        comment_created_at = comment.locator('a[role="link"][tabindex="0"]')
        comment_url = await comment_created_at.get_attribute("href")
        assert comment_url
        comment_id = parse_qs(urlparse(comment_url).query)["comment_id"][0]
        content = await comment.locator('div[dir="auto"]').inner_text()
        return Post(
            provider="facebook",
            post_id=post_id,
            comment_id=comment_id,
            url=comment_url,
            author=profile_name,
            title="",
            content=content,
        )
