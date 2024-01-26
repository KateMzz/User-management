from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8")

    LOGGING_LEVEL: str = Field(default="DEBUG")
    LOGGER_NAME: str = Field(default="user_manager")
    DATABASE: str
    DB_USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    TEST_DB_NAME: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    TEST_REDIS_URL: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    MODE: str
    USER_ID: str
    TOKEN: str
    RABBIT_MQ: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    AWS_S3_BUCKET_NAME: str

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

    @property
    def test_database_url(self) -> str:
        return (
            f"{self.DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"{self.TEST_DB_NAME}"
        )

    @property
    def smtp(self) -> dict:
        return {
            "server": self.SMTP_SERVER,
            "port": self.SMTP_PORT,
            "username": self.SMTP_USERNAME,
            "password": self.SMTP_PASSWORD,
        }


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
