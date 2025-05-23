from lato import Query, TransactionContext

from modules.account import account_module
from modules.account.repository import TeamRepository
from pointsheet.domain import EntityId


class GetTeamQuery(Query):
    team_id: EntityId


@account_module.handler(GetTeamQuery)
def handle_get_team(query: GetTeamQuery, repo: TeamRepository, ctx: TransactionContext):
    team = repo.find_by_id(query.team_id)
    return team or None
