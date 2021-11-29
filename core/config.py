from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str
    mongodb_url: str
    database: str
    secret_key: str
    algorithm: str
    token_expire_minutes: int
    api_key_name: str = "Api-Key"
    modzy_api_key: str
    encryption_key: str


class DevSettings(Settings):
    class Config:
        env_file = "../.env"


class ProdSettings(Settings):
    class Config:
        env_file = ".env.production"


@lru_cache()
def get_settings():
    if Settings().env == "development":
        return DevSettings()
    else:
        return ProdSettings()
