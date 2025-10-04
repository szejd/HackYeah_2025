import logging

from pydantic import field_validator
from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    SERVER_ADDRESS: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    APP_LOG_LEVEL: int = logging.INFO  # Default log level as int

    @field_validator("APP_LOG_LEVEL", mode="before")
    @classmethod
    def parse_log_level(cls, value):
        """Parse log level string to logging constant."""
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "WARN": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            return level_map.get(value.upper(), logging.INFO)

        return logging.INFO

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_config = EnvConfig()
SERVER_ADDRESS = env_config.SERVER_ADDRESS
DB_NAME = env_config.DB_NAME
DB_USER = env_config.DB_USER
DB_PASSWORD = env_config.DB_PASSWORD
APP_LOG_LEVEL = env_config.APP_LOG_LEVEL
