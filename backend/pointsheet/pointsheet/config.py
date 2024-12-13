import os.path
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


instance_path = os.path.join(Path(__file__).parent.parent, "/instance")


class Config(BaseSettings):
    APP_ENV: Optional[str] = "dev"
    DATABASE: Optional[str] = f"sqlite://{instance_path}/point_sheets.db.sqlite"

    model_config = SettingsConfigDict()
