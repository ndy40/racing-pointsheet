from lato import Event

from pointsheet.domain.types import EntityId


class UserRegistered(Event):
    user_id: EntityId
    username: str


class UserRegisteredWithTeam(Event):
    team_name: str
    username: str
    user_id: EntityId
