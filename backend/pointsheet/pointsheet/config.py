import os.path
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

instance_path = os.path.join(Path(__file__).parent.parent, "/instance")


class Config(BaseSettings):
    APP_ENV: Optional[str] = "dev"
    SECRET_KEY: Optional[str] = str(os.urandom(30))
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = 5

    model_config = SettingsConfigDict()
