from lato import Query

from modules.event.repository import TrackRepository
from modules.event import event_module


class GetAllTracks(Query):
    pass


@event_module.handler(GetAllTracks)
def fetch_all_tracks(query: GetAllTracks, repo: TrackRepository):
    result = repo.all()
    return result
