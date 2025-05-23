from lato import Command, TransactionContext

from modules.account import account_module
from modules.account.domain.entity import Team
from modules.account.events import TeamCreated
from modules.account.repository import TeamRepository
from pointsheet.domain import EntityId
from typing import Optional


class CreateTeamCommand(Command):
    name: str
    description: Optional[str] = None
    owner_id: EntityId


@account_module.handler(CreateTeamCommand)
def handle_create_team(
    command: CreateTeamCommand, repo: TeamRepository, ctx: TransactionContext
):
    team = Team(
        name=command.name,
        description=command.description,
        owner_id=command.owner_id,
    )

    repo.add(team)

    ctx.publish(
        TeamCreated(
            team_id=team.id,
            name=team.name,
            owner_id=team.owner_id,
        )
    )
