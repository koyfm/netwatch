from collections.abc import AsyncIterator
from typing import Literal

from netwatch.provider.base import BaseProvider, BaseSource, Post


class FacebookSource(BaseSource):
    provider: Literal["facebook"]


class FacebookProvider(BaseProvider[FacebookSource]):
    def fetch(self) -> AsyncIterator[Post]:
        raise NotImplementedError
