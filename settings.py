from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOGGING_LEVEL: str = Field(default="DEBUG")
    LOGGER_NAME: str = Field(default="user_manager")
    DATABASE: str
    DB_USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB_NAME: str

    class Config:
        env_file = [".env", "../.env"]

    @property
    def database_url(self) -> str:
        return (
            f"{self.DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"{self.DB_NAME}"
        )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
