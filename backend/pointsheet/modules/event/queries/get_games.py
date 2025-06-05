from lato import Query

from modules.event.repository import GameRepository
from modules.event import event_module


class GetGames(Query):
    pass


@event_module.handler(GetGames)
def fetch_all_games(query: GetGames, repo: GameRepository):
    result = repo.all(query)
    return result