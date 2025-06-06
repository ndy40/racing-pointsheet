from typing import Optional
from lato import Query

from modules.event.repository import CarRepository
from modules.event import event_module


class GetCars(Query):
    game_id: int
    page: Optional[int] = 1
    page_size: Optional[int] = 20


@event_module.handler(GetCars)
def fetch_game_cars(query: GetCars, repo: CarRepository):
    # Use the existing CarRepository to fetch cars filtered by game_id with pagination
    result = repo.all(query)
    return result
