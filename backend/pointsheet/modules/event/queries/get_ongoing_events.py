from typing import Optional

from lato import Query

from modules.event import event_module
from modules.event.repository import EventRepository
from pointsheet.domain.types import EntityId


class GetOngoingEvents(Query):
    user_id: Optional[EntityId] = None


@event_module.handler(GetOngoingEvents)
def fetch_ongoing_events(cmd: GetOngoingEvents, repo: EventRepository):
    result = repo.get_ongoing_events(cmd)
    return result
