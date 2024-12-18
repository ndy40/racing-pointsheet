import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database

from pointsheet import config
from pointsheet.db import get_session


@pytest.fixture(scope="session")
def set_env():
    # setup environment variables here instead of a .env file
    os.environ["DATABASE"] = "sqlite:///instance/test.db.sqlite"


@pytest.fixture(scope="session", autouse=True)
def app_config(set_env):
    return config


@pytest.fixture(scope="session")
def setup_database(set_env, app_config):
    # Database URL
    db_url = os.environ["DATABASE"]
    print("db_url ", db_url)
    # Create the database
    create_database(db_url)
    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    # Apply migrations
    command.upgrade(alembic_cfg, "head")
    # yield
    # Drop the database
    # drop_database(db_url)


@pytest.fixture(scope="function")
def db_session():
    _session = get_session()
    try:
        yield _session
    finally:
        _session.rollback()
        _session.close()
