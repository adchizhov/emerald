import os
from functools import lru_cache
from typing import Optional

import pydantic
from environs import Env

env = Env()
env.read_env(path='./.env', override=True)


# Настройки проекта
class Settings(pydantic.BaseSettings):
    PROJECT_NAME: str = 'emerald'
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DEBUG: bool = env.bool('DEBUG')
    APP_HOST: str = env.str('APP_HOST')
    APP_PORT: int = env.int('APP_PORT')
    # redis settings
    REDIS_HOST: str = env.str('REDIS_HOST')
    REDIS_PORT: int = env.int('REDIS_PORT')
    REDIS_DATABASE: int = env.int('REDIS_DATABASE')
    REDIS_URL: Optional[str] = None

    # Ключ под которым хранится счетчик в кэше редис
    COUNTER_KEY: str = env.str('COUNTER_KEY', default='counter')

    # cdn host settings
    CDN_HOST: str = env.str('CDN_HOST')

    # logging settings
    LOG_LEVEL: str = env.str('LOG_LEVEL', default='DEBUG')
    LOG_LEVEL_ROOT: str = env.str('LOG_LEVEL_ROOT', default='DEBUG')
    LOG_LEVEL_PROJECT_NAME: str = env.str('LOG_LEVEL_PROJECT_NAME', default='DEBUG')

    @pydantic.validator('REDIS_URL', pre=True, always=True)
    def default_REDIS_URL(cls, value, *, values, **kwargs):
        database_url = value or (f'redis://{values["REDIS_HOST"]}:{values["REDIS_PORT"]}/{values["REDIS_DATABASE"]}')
        return database_url


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
