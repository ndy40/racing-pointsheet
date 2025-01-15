from datetime import datetime, timedelta

import pytest
import sqlalchemy.event
from sqlalchemy.orm import scoped_session, sessionmaker

from pointsheet import create_app
from pointsheet.db import engine
from pointsheet.factories.event import EventFactory, SeriesFactory
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


@pytest.fixture()
def app(db_session):
    app = create_app()

    yield app


@pytest.fixture()
def client(app):
    app.testing = True
    return app.test_client()


@pytest.fixture
def event_factory(db_session) -> EventFactory:
    EventFactory._meta.sqlalchemy_session_factory = lambda: db_session
    return EventFactory


@pytest.fixture
def series_factory(db_session) -> SeriesFactory:
    SeriesFactory._meta.sqlalchemy_session_factory = lambda: db_session
    return SeriesFactory


@pytest.fixture
def start_end_date_future() -> tuple[datetime, datetime]:
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=20)
    return start_date, end_date
