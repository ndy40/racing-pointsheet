from uuid import uuid4

from modules.event.domain.entity import Event as EventModel
from modules.event.domain.value_objects import EventStatus
from modules.event.repository import EventModelMapper
from pointsheet.models import Event


def test_event_data_mapper():
    event_model = EventModel(title="Event1", status=EventStatus.open, host=uuid4())

    mapper = EventModelMapper().to_db_entity(event_model)

    assert isinstance(mapper, Event)
