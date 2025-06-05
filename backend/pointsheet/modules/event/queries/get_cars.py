from lato import Query

from modules.event.repository import CarRepository
from modules.event import event_module


class GetCars(Query):
    game_id: int


@event_module.handler(GetCars)
def fetch_game_cars(query: GetCars, repo: CarRepository):
    # Use the existing CarRepository to fetch cars filtered by game_id
    result = repo.all(query)
    return result