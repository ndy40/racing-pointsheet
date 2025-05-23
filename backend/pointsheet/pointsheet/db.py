from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from pointsheet.config import Config

_config = Config()

engine = create_engine(
    _config.DATABASE,
    connect_args={"check_same_thread": False},
    pool_size=20,
    pool_recycle=3600,
    pool_pre_ping=True,
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
