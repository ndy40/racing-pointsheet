import pytest

from modules.event.domain.entity import Event as EventModel
from modules.event.domain.value_objects import EventStatus
from modules.event.repository import EventModelMapper
from pointsheet.models import Event


@pytest.mark.skip
def test_event_data_mapper():
    event_model = EventModel(title="Event1", status=EventStatus.open)

    mapper = EventModelMapper().from_model(event_model)

    assert mapper is Event
