from lato import Query

from modules.event import event_module
from modules.event.repository import EventRepository


class GetEvents(Query):
    pass


@event_module.handler(GetEvents)
def fetch_all_events(repo: EventRepository):
    result = repo.all()
    return result
