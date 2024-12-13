from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pointsheet.config import Config


_config = Config()

engine = create_engine(_config.DATABASE)
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)


def get_session():
    return Session()
