from typing import List

from modules.event import event_module
from modules.event.domain.queries import GetAllSeries


@event_module.handler(GetAllSeries)
def fetch_all_series(query: GetAllSeries) -> List[str]:
    print("this got called")
    return ["s1", "s2"]
