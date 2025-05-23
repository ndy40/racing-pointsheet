from lato import Command, TransactionContext

from modules.account import account_module
from modules.account.domain.exceptions import (
    AlreadyTeamMemberException,
    NotTeamOwnerException,
)
from modules.account.events import DriverJoinedTeam
from modules.account.repository import TeamRepository
from pointsheet.domain.types import EntityId


class AddTeamMemberCommand(Command):
    team_id: EntityId
    driver_id: EntityId
    role: str = "member"
    requester_id: EntityId  # The user making the request


@account_module.handler(AddTeamMemberCommand)
def handle_add_team_member(
    command: AddTeamMemberCommand, repo: TeamRepository, ctx: TransactionContext
):
    team = repo.find_by_id(command.team_id)

    if not team:
        return {"error": "Team not found"}

    if team.owner_id != command.requester_id:
        raise NotTeamOwnerException()

    if team.is_member(command.driver_id):
        raise AlreadyTeamMemberException()

    ctx.publish(
        DriverJoinedTeam(
            team_id=command.team_id,
            driver_id=command.driver_id,
            role=command.role,
        )
    )

    return {"success": True}
