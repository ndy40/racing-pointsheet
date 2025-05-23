from uuid import UUID

from lato import Query

from modules.event import event_module
from modules.event.repository import SeriesRepository


class GetSeriesById(Query):
    id: UUID


@event_module.handler(GetSeriesById)
def get_series_by_id(cmd: GetSeriesById, repo: SeriesRepository):
    series = repo.find_by_id(id=cmd.id)
    return series or None
