from uuid import UUID

from lato import Query

from modules import event_module
from modules.event.dependencies import container
from modules.event.repository import SeriesRepository


class GetSeriesById(Query):
    id: UUID


@event_module.handler(GetSeriesById)
def get_series_by_id(cmd: GetSeriesById):
    series_repo: SeriesRepository = container[SeriesRepository]
    series = series_repo.find_by_id(id=cmd.id)
    return series
