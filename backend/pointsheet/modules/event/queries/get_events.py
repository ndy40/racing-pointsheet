from lato import Query

from modules import event_module
from modules.event.dependencies import container
from modules.event.repository import EventRepository


class GetEvents(Query):
    pass


@event_module.handler(GetEvents)
def fetch_all_events():
    repo = container[EventRepository]
    result = repo.all()
    return result
