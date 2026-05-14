from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Sample fast api"
    VERSION:str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()