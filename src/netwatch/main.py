import logging
from inspect import get_annotations
from types import get_original_bases
from typing import get_args
from netwatch.config import settings
from netwatch.provider.base import BaseProvider

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    provider_cls_map = {}
    for provider_cls in BaseProvider.__subclasses__():
        base_provider = get_original_bases(provider_cls)[0]
        provider_args = get_args(base_provider)
        if not provider_args:
            log.error(f"Could not determine source type for provider {provider_cls}")
            continue
        base_source = provider_args[0]
        annotations = get_annotations(base_source)
        source_provider_args = get_args(annotations.get("provider"))
        if not source_provider_args:
            log.error(f"Could not determine provider for source {base_source}")
            continue
        provider = source_provider_args[0]
        provider_cls_map[provider] = provider_cls

    providers = []
    for source in settings.sources:
        provider_cls = provider_cls_map.get(source.provider)
        assert provider_cls is not None
        provider = provider_cls(source)
        providers.append(provider)

    log.info(f"Initialized {len(providers)} providers")
