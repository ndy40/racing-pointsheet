from typing import List, Optional

from lato import Query

from modules.event import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from modules.event.domain.value_objects import SeriesStatus
from modules.event.repository import SeriesRepository


class GetAllSeries(Query):
    status: Optional[SeriesStatus] = None


@event_module.handler(GetAllSeries)
def fetch_all_series(query: GetAllSeries) -> List[Event]:
    repository = container[SeriesRepository]
    result = repository.all(query)
    return result
