from typing import Literal
from netwatch.provider.base import BaseProvider, BaseSource


class FacebookSource(BaseSource):
    provider: Literal["facebook"]


class FacebookProvider(BaseProvider[FacebookSource]):
    def fetch(self):
        raise NotImplementedError
