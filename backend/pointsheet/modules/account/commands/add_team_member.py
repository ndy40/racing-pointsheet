from lato import Command

from modules.account import account_module
from modules.account.domain.exceptions import (
    AlreadyTeamMemberException,
    NotTeamOwnerException,
)
from modules.account.events import DriverJoinedTeam
from modules.account.repository import TeamRepository
from pointsheet.domain import EntityId
from pointsheet.events import EventBus


class AddTeamMemberCommand(Command):
    team_id: EntityId
    driver_id: EntityId
    role: str = "member"
    requester_id: EntityId  # The user making the request


@account_module.handler(AddTeamMemberCommand)
def handle_add_team_member(
    command: AddTeamMemberCommand, repo: TeamRepository, event_bus: EventBus
):
    team = repo.find_by_id(command.team_id)

    if not team:
        return {"error": "Team not found"}

    if team.owner_id != command.requester_id:
        raise NotTeamOwnerException()

    if team.is_member(command.driver_id):
        raise AlreadyTeamMemberException()

    event_bus.publish(
        DriverJoinedTeam(
            team_id=command.team_id,
            driver_id=command.driver_id,
            role=command.role,
        )
    )

    return {"success": True}
