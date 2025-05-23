from lato import Query

from modules.event import event_module
from modules.event.repository import EventRepository


class GetRecentEvent(Query):
    driver_id: int


@event_module.handler(GetRecentEvent)
def handle_get_recent_event(query: GetRecentEvent, event_repo: EventRepository):
    pass
