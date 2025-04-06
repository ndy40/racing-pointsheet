from lato import Query

from modules import event_module
from modules.event.repository import EventRepository


class GetAvailableEvents(Query):
    pass


@event_module.handler(GetAvailableEvents)
def handle_get_available_events(event: GetAvailableEvents, repo: EventRepository):
    return repo.get_available_events()
