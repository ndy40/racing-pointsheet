from modules import account_module, UserRepository
from modules.account.domain.entity import Driver
from modules.account.events import DriverJoinedTeam, DriverLeftTeam
from modules.account.repository import TeamRepository
from modules.auth.events.user_registered import UserRegistered


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


@account_module.handler(UserRegistered)
def handle_registered_user(event: UserRegistered, repo: UserRepository):
    user = Driver(id=event.user_id)
    repo.add(user)
