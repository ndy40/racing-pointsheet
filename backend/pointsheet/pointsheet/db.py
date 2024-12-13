from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pointsheet import config

engine = create_engine(config.DATABASE)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine), )

def get_session():
    return Session()