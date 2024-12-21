from typing import List

from modules.event import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from modules.event.domain.queries import GetAllSeries
from modules.event.repository import EventRepository


@event_module.handler(GetAllSeries)
def fetch_all_series(query: GetAllSeries) -> List[Event]:
    repository = container[EventRepository]
    return repository.all()
