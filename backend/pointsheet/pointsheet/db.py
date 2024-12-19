from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pointsheet.config import Config

_config = Config()

engine = create_engine(_config.DATABASE)
Session = sessionmaker(
    engine,
)


def get_session():
    return Session()
