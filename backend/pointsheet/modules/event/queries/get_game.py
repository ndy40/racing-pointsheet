from lato import Query

from modules.event.repository import GameRepository
from modules.event import event_module


class GetGame(Query):
    game_id: int


@event_module.handler(GetGame)
def fetch_game(query: GetGame, repo: GameRepository):
    result = repo.find_by_id(query.game_id)
    return result