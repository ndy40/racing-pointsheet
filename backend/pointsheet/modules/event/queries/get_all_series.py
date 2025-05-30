from typing import List, Optional

from lato import Query

from modules.event import event_module
from modules.event.domain.entity import Series
from modules.event.domain.value_objects import SeriesStatus
from modules.event.repository import SeriesRepository


class GetAllSeries(Query):
    status: Optional[List[SeriesStatus]] = None


@event_module.handler(GetAllSeries)
def fetch_all_series(query: GetAllSeries, repository: SeriesRepository) -> List[Series]:
    result = repository.all(query)
    return result
