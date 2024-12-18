import logging

import pytest
from flask.cli import load_dotenv

from pointsheet import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv(path=".env.test")


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # setup environment variables here instead of a .env file
    monkeypatch.setenv("DATABASE", "sqlite:///:memory:")


@pytest.fixture(scope="session", autouse=True)
def app_config(set_env):
    return config


@pytest.fixture(scope="session")
def initialize_db(app_config, set_env):
    print(app_config.model_dump())
    logger.info("Session started")
