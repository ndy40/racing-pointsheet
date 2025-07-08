from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from pointsheet.config import config


engine = create_engine(
    config.DATABASE,
    connect_args={"check_same_thread": False},
    pool_size=10,
    # max_overflow=5,
    pool_recycle=1800,
    pool_pre_ping=True,
    # pool_timeout=30,
    echo_pool=False,
)

# Create a sessionmaker that can be used to create sessions
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def get_session():
    """Context manager for database sessions."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# In db.py
from flask import g
from contextlib import contextmanager

@contextmanager
def request_session():
    """Get a session for the current request."""
    if 'db_session' not in g:
        g.db_session = Session()

    try:
        yield g.db_session
        g.db_session.commit()
    except Exception:
        g.db_session.rollback()
        raise
