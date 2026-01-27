from collections.abc import AsyncIterator
from typing import Literal

from netwatch.provider.base import BaseProvider, BaseSource, Post


class RSSSource(BaseSource):
    provider: Literal["rss"]


class RSSProvider(BaseProvider[RSSSource]):
    def fetch(self) -> AsyncIterator[Post]:
        raise NotImplementedError
