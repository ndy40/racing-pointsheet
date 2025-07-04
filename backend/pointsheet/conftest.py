from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
import sqlalchemy.event
from sqlalchemy.orm import scoped_session, sessionmaker

from modules.auth.repository import RegisterUserRepository
from pointsheet import create_app
from pointsheet.db import engine
from pointsheet.models import BaseModel


@pytest.fixture
def setup_database():
    BaseModel.metadata.create_all(bind=engine)
    yield
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    TestSessionLocal = scoped_session(
        sessionmaker(bind=engine, autoflush=False, autocommit=False)
    )
    session = TestSessionLocal()

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


@pytest.fixture(scope="function", autouse=True)
def patch_session(db_session):
    # Create a generator function that yields the test session
    def mock_get_session():
        yield db_session

    # Patch get_session to use our mock function
    with patch("pointsheet.db.get_session", mock_get_session) as session:
        # Patch the Session object
        with patch("pointsheet.db.Session") as mock_session:
            # Configure the mock to return the test session when called
            mock_session.return_value = db_session
            # Also patch the remove method to prevent closing the session
            mock_session.remove = lambda: None

            yield session


@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app


@pytest.fixture(
    scope="module",
    autouse=True,
)
def client(app):
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def start_end_date_future() -> tuple[datetime, datetime]:
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=20)
    return start_date, end_date


@pytest.fixture(scope="function", autouse=True)
def default_user(db_session):
    from modules.auth.domain import RegisteredUser

    new_user = RegisteredUser(username="testuser", password="password1")
    repo = RegisterUserRepository(db_session)
    repo.add(new_user)
    db_session.commit()
    return new_user


@pytest.fixture(scope="function", autouse=True)
def login(client):
    response = client.post(
        "/api/auth",
        json={"username": "testuser", "password": "password1"},
    )
    return response.json


@pytest.fixture(scope="function")
def auth_token(login):
    return {"Authorization": f"Bearer {login['token']}"}


@pytest.fixture(scope="function", autouse=True)
def current_user(default_user):
    with patch("modules.get_user_id") as mock_get_current_user:
        mock_get_current_user.return_value = default_user.id
        yield default_user
