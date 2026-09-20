import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SIH26017 Land Acquisition Delay & Risk Engine"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend/app/db/projects.db")
    ALERT_RISK_THRESHOLD: int = 70
    CORS_ORIGINS: list = ["*"]

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()


