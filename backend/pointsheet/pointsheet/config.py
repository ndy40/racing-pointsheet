import os.path
from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from pointsheet.storage import LocalFileStore

work_dir = Path(__file__).parent.parent

instance_path = os.path.join(work_dir, "/instance")


SEVEN_DAYS_IN_SECONDS: int = 60 * 24 * 7


class Config(BaseSettings):
    SECRET_KEY: str
    APP_ENV: Optional[str] = "development"
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = SEVEN_DAYS_IN_SECONDS
    UPLOAD_FOLDER: Optional[str] = "uploads/"
    BROKER_URL: Optional[str]
    RESULT_BACKEND: Optional[str] = "db+sqlite:///instance/task_result.db.sqlite"
    GOOGLE_API_KEY: Optional[str] = "AIzaSyCQ2glxUjVNTd3FzrpR0v79pIj8UXeNd3w"
    SENTRY_DSN: Optional[str] = None
    WTF_CSRF_CHECK_DEFAULT: bool = True
    WTF_CSRF_EXEMPT_ROUTES: List[str] = ["/api/*"]

    model_config = SettingsConfigDict()

    @property
    def file_store(self):
        # switch context depending on ENV
        return LocalFileStore(base_path=self.UPLOAD_FOLDER)


config = Config()
