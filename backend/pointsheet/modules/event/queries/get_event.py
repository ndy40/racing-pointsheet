from lato import Query

from modules import event_module
from modules.event.dependencies import container
from modules.event.repository import EventRepository
from pointsheet.domain import EntityId


class GetEvent(Query):
    event_id: EntityId


@event_module.handler(GetEvent)
def get_event(cmd: GetEvent):
    repository = container[EventRepository]
    result = repository.find_by_id(cmd.event_id)
    return result
