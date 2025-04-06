from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from pointsheet.config import Config

_config = Config()

engine = create_engine(_config.DATABASE)
Session = scoped_session(
    sessionmaker(
        engine,
    )
)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
