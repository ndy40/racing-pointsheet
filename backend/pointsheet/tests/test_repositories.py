from modules.event.domain.entity import Event
from modules.event.domain.value_objects import EntityId, EventStatus
from modules.event.repository import EventRepository


def test_saving_of_event_using_repository(db_session):
    event = Event(title="Event 1", status=EventStatus.open, host=EntityId(int=1))
    event_repo = EventRepository(db_session)
    event_repo.add(event)
    db_session.commit()
