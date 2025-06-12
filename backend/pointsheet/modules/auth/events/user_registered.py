from lato import Event

from pointsheet.domain.entity import UserRole
from pointsheet.domain.types import EntityId


class UserRegistered(Event):
    user_id: EntityId
    username: str
    role: UserRole


class UserRegisteredWithTeam(Event):
    team_name: str
    username: str
    user_id: EntityId
    role: UserRole