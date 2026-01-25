from typing import Literal
from netwatch.provider.base import BaseProvider, BaseSource


class RSSSource(BaseSource):
    provider: Literal["rss"]


class RSSProvider(BaseProvider[RSSSource]):
    def fetch(self):
        raise NotImplementedError
