from typing import List

from lato import Query

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from modules.event.repository import SeriesRepository


class GetAllSeries(Query): ...


@event_module.handler(GetAllSeries)
def fetch_all_series(query: GetAllSeries) -> List[Event]:
    repository = container[SeriesRepository]
    result = repository.all()
    return result
