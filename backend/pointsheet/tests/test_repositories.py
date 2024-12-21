import pytest

from modules.event.domain.entity import Event
from modules.event.domain.value_objects import EntityId, EventStatus
from modules.event.repository import EventRepository
from pointsheet.factories.event import EventFactory
from pointsheet.models.event import Event as EventModel


@pytest.fixture
def event_factory(db_session) -> EventFactory:
    EventFactory._meta.sqlalchemy_session_factory = lambda: db_session
    return EventFactory


def test_saving_of_event_using_repository(db_session):
    event = Event(title="Event 1", status=EventStatus.open, host=EntityId(int=1))
    event_repo = EventRepository(db_session)
    event_repo.add(event)
    db_session.commit()


def test_fetching_of_model_using_repository(db_session, event_factory):
    user_factory: EventModel = event_factory()
    db_session.commit()

    id = user_factory.id

    inserted_model = EventRepository(db_session).find_by_id(id)

    assert id == inserted_model.id


def test_fetching_all_event_using_repository(db_session, event_factory):
    event_factory()
    event_factory()
    db_session.commit()

    result = EventRepository(db_session).all()

    assert len(result) == 2
