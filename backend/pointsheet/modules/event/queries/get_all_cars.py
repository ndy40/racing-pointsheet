from typing import Optional

from lato import Query

from modules.event.repository import CarRepository
from modules.event import event_module


class GetAllCars(Query):
    game: Optional[str] = None


@event_module.handler(GetAllCars)
def fetch_all_cars(query: GetAllCars, repo: CarRepository):
    result = repo.all(query)
    return result