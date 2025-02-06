import os.path
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from pointsheet.storage import LocalFileStore

work_dir = Path(__file__).parent.parent

instance_path = os.path.join(work_dir, "/instance")

upload_dir = os.path.join(work_dir, "/uploads")


SEVEN_DAYS_IN_SECONDS: int = 60 * 24 * 7


class Config(BaseSettings):
    SECRET_KEY: str
    APP_ENV: Optional[str] = "dev"
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = SEVEN_DAYS_IN_SECONDS
    UPLOAD_FOLDER: Optional[str] = Field(
        default=upload_dir,
        description="Upload folder for files",
    )
    QUEUE_BROKER: Optional[str]
    BROKER_BACKEND: Optional[str] = "db+sqlite:///instance/task_result.db.sqlite"

    model_config = SettingsConfigDict()

    @property
    def file_store(self):
        # switch context depending on ENV
        return LocalFileStore(base_path=self.UPLOAD_FOLDER)


config = Config()
