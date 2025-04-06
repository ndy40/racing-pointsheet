from lato import Query

from modules.event import event_module
from modules.event.repository import EventRepository


class GetOngoingEvents(Query):
    pass


@event_module.handler(GetOngoingEvents)
def fetch_ongoing_events(cmd: GetOngoingEvents, repo: EventRepository):
    result = repo.get_ongoing_events()
    return result
