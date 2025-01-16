import os.path
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

instance_path = os.path.join(Path(__file__).parent.parent, "/instance")

SEVEN_DAYS_IN_SECONDS: int = 60 * 24 * 7


class Config(BaseSettings):
    SECRET_KEY: str
    APP_ENV: Optional[str] = "dev"
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = SEVEN_DAYS_IN_SECONDS

    model_config = SettingsConfigDict()


config = Config()
