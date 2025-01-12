import os.path
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

instance_path = os.path.join(Path(__file__).parent.parent, "/instance")

SEVENT_DAYS_IN_SECONDS = 60 * 60 * 24 * 7


class Config(BaseSettings):
    APP_ENV: Optional[str] = "dev"
    SECRET_KEY: Optional[str] = str(os.urandom(30))
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = SEVENT_DAYS_IN_SECONDS

    model_config = SettingsConfigDict()


config = Config()
