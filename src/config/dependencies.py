import functools

import src.config.settings as settings


@functools.lru_cache()
def get_api_settings() -> settings.APISettings:
    return settings.APISettings()


@functools.lru_cache()
def get_db_settings() -> settings.DataBaseSettings:
    return settings.DataBaseSettings()


def get_db_url() -> str:
    db_settings = get_db_settings()
    return f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.db}"


def get_db_url_sync() -> str:
    db_settings = get_db_settings()
    return f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.db}"
