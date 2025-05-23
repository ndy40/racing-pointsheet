from dataclasses import dataclass

from lato import Event

from pointsheet.domain import EntityId


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
