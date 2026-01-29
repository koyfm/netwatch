from abc import abstractmethod
from collections.abc import AsyncIterator

from pydantic import BaseModel


class BaseSource(BaseModel):
    pass


class Post(BaseModel):
    provider: str
    post_id: str
    comment_id: str
    url: str
    author: str
    title: str
    content: str


class BaseProvider[T: BaseSource]:
    def __init__(self, source: T) -> None:
        self.source = source

    @abstractmethod
    def fetch(self, **kwargs) -> AsyncIterator[Post]:
        raise NotImplementedError
