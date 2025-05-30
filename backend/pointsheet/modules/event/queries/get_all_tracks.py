from enum import Enum

from lato import Query

from modules.event.repository import TrackRepository
from modules.event import event_module


class OrderBy(Enum):
    id = "id"
    name = "name"

class Direction(Enum):
    asc = "asc"
    desc = "desc"

class GetAllTracks(Query):
    order_by: OrderBy = OrderBy.id
    direction: Direction = Direction.asc


@event_module.handler(GetAllTracks)
def fetch_all_tracks(query: GetAllTracks, repo: TrackRepository):
    result = repo.all(order=query)
    return result
