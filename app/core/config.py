from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "sample fastapi backend"
    VERSION:str = "1.0.1"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()