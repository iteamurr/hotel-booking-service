import pydantic_settings


class BaseSettings(pydantic_settings.BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class APISettings(BaseSettings):
    title: str
    host: str
    port: int

    class Config(BaseSettings.Config):
        env_prefix = "API_"
        extra = "allow"


class DataBaseSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    class Config(BaseSettings.Config):
        env_prefix = "POSTGRES_"
        extra = "allow"
