import multiprocessing
from functools import lru_cache

from pydantic import BaseSettings, MongoDsn, Field


class ServerConfig(BaseSettings):
    app_name: str = "APP_NAME"
    host: str = Field(None, env="HOST")
    port: int = Field(None, env="PORT")
    debug_mode: bool = Field(None, env="DEBUG")
    workers: int = multiprocessing.cpu_count() * 2 + 1

    # """JWT CONFIG"""
    jwt_secret: str = Field(None, env="JWT_SECRET")
    jwt_algorithm: str = Field(None, env="JWT_ALGORITHM")
    jwt_expiration_delta: int = Field(None, env="JWT_EXPIRATION_DELTA")
    jwt_refresh_expiration_delta: int = Field(None, env="JWT_REFRESH_EXPIRATION_DELTA")

    # """AES CIHPER CONFIG"""
    aes_key: str = Field(None, env="AES_KEY")
    aes_iv: str = Field(None, env="AES_IV")


class GlobalConfig(ServerConfig):
    ENVIRONMENT: str | None = Field(None, env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DevConfig(GlobalConfig):
    """Development configuration"""

    class Config:
        env_file = [".env", "envs/.env.dev"]


class ProdConfig(GlobalConfig):
    """Production configuration"""

    class Config:
        env_file = [".env", "envs/.env.prod"]


class LocalConfig(GlobalConfig):
    """Local configuration"""

    class Config:
        env_file = [".env", "envs/.env.local"]


class FactoryConfig:
    """Returns a config instance dependence on the ENV_STATE variable."""

    def __init__(self):
        self.env_state = GlobalConfig().ENVIRONMENT

    def __call__(self):
        match self.env_state:
            case "dev":
                return DevConfig()
            case "prod":
                return ProdConfig()
            case "local":
                return LocalConfig()
            case _:
                return GlobalConfig()


@lru_cache()
def get_config() -> GlobalConfig:
    """Returns a config instance dependence on the ENV_STATE variable."""
    return FactoryConfig()()


settings = get_config()
