from modules.event.domain.entity import Event
from modules.event.domain.value_objects import EventStatus
from pointsheet.domain.types import EntityId
from modules.event.repository import EventRepository
from pointsheet.factories.event import EventFactory


def test_saving_of_event_using_repository(db_session):
    event = Event(title="Event 1", status=EventStatus.open, host=EntityId(int=1))
    event_repo = EventRepository(db_session)
    event_repo.add(event)
    db_session.commit()


def test_fetching_of_model_using_repository(db_session):
    event = EventFactory(session=db_session)

    event_id = event.id
    inserted_model = EventRepository(db_session).find_by_id(event.id)

    assert event_id == inserted_model.id


def test_fetching_all_event_using_repository(db_session):
    EventFactory(session=db_session)
    EventFactory(session=db_session)
    db_session.commit()

    result = EventRepository(db_session).all()

    assert len(result) == 2
