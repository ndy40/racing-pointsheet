import os.path
from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from pointsheet.storage import LocalFileStore, S3FileStore

work_dir = Path(__file__).parent.parent

instance_path = os.path.join(work_dir, "/instance")


SEVEN_DAYS_IN_SECONDS: int = 60 * 24 * 7


class Config(BaseSettings):
    SECRET_KEY: str
    APP_ENV: Optional[str] = "development"
    DOMAIN: Optional[str] = "http://pointsheet-app.com"
    DATABASE: Optional[str]
    AUTH_TOKEN_MAX_AGE: Optional[int] = SEVEN_DAYS_IN_SECONDS
    UPLOAD_FOLDER: Optional[str] = "uploads/"
    BROKER_URL: Optional[str]
    RESULT_BACKEND: Optional[str] = "db+sqlite:///instance/task_result.db.sqlite"
    GOOGLE_API_KEY: Optional[str] = "AIzaSyCQ2glxUjVNTd3FzrpR0v79pIj8UXeNd3w"
    SENTRY_DSN: Optional[str] = None
    WTF_CSRF_CHECK_DEFAULT: bool = False
    WTF_CSRF_EXEMPT_ROUTES: List[str] = ["/api/*"]
    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True
    # AWS S3 configuration
    AWS_BUCKET_NAME: Optional[str] = None
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    CLOUDFRONT_DOMAIN: Optional[str] = None
    model_config = SettingsConfigDict()

    @property
    def file_store(self):
        # switch context depending on ENV
        if self.APP_ENV == "development":
            return LocalFileStore(base_path=self.UPLOAD_FOLDER)
        else:
            if not self.AWS_BUCKET_NAME:
                raise ValueError(
                    "AWS_BUCKET_NAME must be set for non-development environments"
                )
            return S3FileStore(
                bucket_name=self.AWS_BUCKET_NAME,
                base_path=self.UPLOAD_FOLDER,
                region_name=self.AWS_REGION,
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            )


config = Config()
