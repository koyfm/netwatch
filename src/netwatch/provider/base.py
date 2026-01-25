from pydantic import BaseModel


class BaseSource(BaseModel):
    pass


class BaseProvider[T: BaseSource]:
    def __init__(self, source: T) -> None:
        self.source = source

    def fetch(self):
        raise NotImplementedError
