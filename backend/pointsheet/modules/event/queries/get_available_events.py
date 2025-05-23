from typing import Optional

from lato import Query

from modules.event import event_module
from modules.event.repository import EventRepository
from pointsheet.domain.types import EntityId


class GetAvailableEvents(Query):
    user_id: Optional[EntityId]


@event_module.handler(GetAvailableEvents)
def handle_get_available_events(event: GetAvailableEvents, repo: EventRepository):
    return repo.get_available_events(event)
