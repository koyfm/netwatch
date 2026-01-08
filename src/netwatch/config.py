from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///netwatch.db"


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")


settings = Settings()
