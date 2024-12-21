import pytest
import sqlalchemy.event
from sqlalchemy.orm import scoped_session, sessionmaker

from pointsheet.db import engine
from pointsheet.models import BaseModel


@pytest.fixture
def setup_database():
    BaseModel.metadata.create_all(bind=engine)
    yield
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    TestSessionLocal = scoped_session(
        sessionmaker(bind=engine, autoflush=False, autocommit=False)
    )
    session = TestSessionLocal(bind=engine)

    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
