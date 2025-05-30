from lato import Query
from sqlalchemy import select

from modules.event.repository import TrackRepository
from modules.event import event_module
from pointsheet.models import Track


class GetTrackById(Query):
    track_id: int


@event_module.handler(GetTrackById)
def fetch_track_by_id(query: GetTrackById, repo: TrackRepository):
    """
    Fetch a track by its ID.

    Args:
        query: The query containing the track_id
        repo: The track repository

    Returns:
        The track if found, None otherwise
    """
    return repo.find_by_id(query.track_id)
