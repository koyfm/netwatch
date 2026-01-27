from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from netwatch.provider.facebook import FacebookSource
from netwatch.provider.rss import RSSSource

SourceConfig = Annotated[
    FacebookSource | RSSSource,
    Field(discriminator="provider"),
]


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///netwatch.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")

    database: DatabaseConfig = DatabaseConfig()
    sources: list[SourceConfig] = []


settings = Settings()
