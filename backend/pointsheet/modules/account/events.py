from lato import Event

from pointsheet.domain.types import EntityId


class TeamCreated(Event):
    team_id: EntityId
    name: str
    owner_id: EntityId


class DriverJoinedTeam(Event):
    team_id: EntityId
    driver_id: EntityId
    role: str


class DriverLeftTeam(Event):
    team_id: EntityId
    driver_id: EntityId


class DriverRegistered(Event):
    driver_id: EntityId
