import logging
from enum import StrEnum

from pydantic import field_validator
from pydantic_settings import BaseSettings


class DBType(StrEnum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class EnvConfig(BaseSettings):
    DB_TYPE: DBType = DBType.SQLITE
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432
    APP_LOG_LEVEL: int = logging.INFO  # Default log level as int

    # JWT Settings
    JWT_SECRET_KEY: str = ""  # Change this in production!
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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

    @field_validator("DB_TYPE", mode="before")
    @classmethod
    def validate_db_type(cls, value):
        """Validate and parse the database type."""
        if isinstance(value, DBType):
            return value

        if isinstance(value, str):
            try:
                # Try to match by value (e.g., "sqlite" or "postgresql")
                for db_type in DBType:
                    if db_type.value.lower() == value.lower():
                        return db_type
                # If not found, raise error
                valid_values = ", ".join([dt.value for dt in DBType])
                raise ValueError(f"Invalid DB_TYPE: {value}. Valid values: {valid_values}")
            except Exception as e:
                if isinstance(e, ValueError):
                    raise
                raise ValueError(f"Invalid DB_TYPE: {value}")

        raise ValueError(f"Invalid DB_TYPE: {value}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_config = EnvConfig()
DB_HOST = env_config.DB_HOST
DB_TYPE = env_config.DB_TYPE
DB_NAME = env_config.DB_NAME
DB_USER = env_config.DB_USER
DB_PASSWORD = env_config.DB_PASSWORD
DB_PORT = env_config.DB_PORT
APP_LOG_LEVEL = env_config.APP_LOG_LEVEL
JWT_SECRET_KEY = env_config.JWT_SECRET_KEY
JWT_ALGORITHM = env_config.JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = env_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
