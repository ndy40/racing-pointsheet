from lato import TransactionContext

from modules.account import account_module
from modules.account.commands.create_team import CreateTeamCommand
from modules.account.domain.entity import Driver
from modules.account.events import DriverJoinedTeam, DriverLeftTeam, DriverRegistered
from modules.account.repository import TeamRepository, DriverRepository
from modules.auth.events.user_registered import UserRegistered, UserRegisteredWithTeam


@account_module.handler(DriverJoinedTeam)
def handle_driver_joined_team(
    event: DriverJoinedTeam, user_repo: DriverRepository, team_repo: TeamRepository
):
    driver = user_repo.find_by_id(event.driver_id)
    team = team_repo.find_by_id(event.team_id)

    if driver and team:
        driver.join_team(event.team_id)
        team.add_member(event.driver_id, event.role)

        user_repo.update(driver)
        team_repo.update(team)


@account_module.handler(DriverLeftTeam)
def handle_driver_left_team(
    event: DriverLeftTeam, user_repo: DriverRepository, team_repo: TeamRepository
):
    driver = user_repo.find_by_id(event.driver_id)
    team = team_repo.find_by_id(event.team_id)

    if driver and team and driver.team_id == event.team_id:
        driver.leave_team()
        team.remove_member(event.driver_id)

        user_repo.update(driver)
        team_repo.update(team)


@account_module.handler(UserRegistered)
def handle_registered_user(event: UserRegistered, repo: DriverRepository):
    user = Driver(id=event.user_id, name=event.username, role=event.role)
    repo.add(user)


@account_module.handler(UserRegisteredWithTeam)
def handle_register_user_with_team(
    event: UserRegisteredWithTeam, repo: DriverRepository, ctx: TransactionContext
):
    user = Driver(id=event.user_id, name=event.username)
    repo.add(user)

    ctx.publish(DriverRegistered(driver_id=event.user_id))
    ctx.publish(CreateTeamCommand(name=event.team_name, owner_id=event.user_id))
