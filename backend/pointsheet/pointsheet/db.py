from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pointsheet.config import Config


_config = Config()

engine = create_engine(_config.DATABASE)
Session = scoped_session(
    sessionmaker(engine),
)
_session = None


def get_session():
    global _session

    if not _session:
        _session = Session()
    return _session
