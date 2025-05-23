from dataclasses import dataclass

from lato import Event

from modules.account import account_module
from modules.account.domain.entity import Driver
from modules.account.repository import UserRepository, TeamRepository
from modules.auth.events.user_registered import UserRegistered
from pointsheet.domain import EntityId


@account_module.handler(UserRegistered)
def handle_registered_user(event: UserRegistered, repo: UserRepository):
    user = Driver(id=event.user_id)
    repo.add(user)


@dataclass
class TeamCreated(Event):
    team_id: EntityId
    name: str
    owner_id: EntityId


@dataclass
class DriverJoinedTeam(Event):
    team_id: EntityId
    driver_id: EntityId
    role: str


@dataclass
class DriverLeftTeam(Event):
    team_id: EntityId
    driver_id: EntityId


@account_module.handler(DriverJoinedTeam)
def handle_driver_joined_team(
    event: DriverJoinedTeam, user_repo: UserRepository, team_repo: TeamRepository
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
    event: DriverLeftTeam, user_repo: UserRepository, team_repo: TeamRepository
):
    driver = user_repo.find_by_id(event.driver_id)
    team = team_repo.find_by_id(event.team_id)

    if driver and team and driver.team_id == event.team_id:
        driver.leave_team()
        team.remove_member(event.driver_id)

        user_repo.update(driver)
        team_repo.update(team)
