from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVER_ADDRESS: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    APP_LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
SERVER_ADDRESS = settings.SERVER_ADDRESS
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
APP_LOG_LEVEL = settings.APP_LOG_LEVEL
