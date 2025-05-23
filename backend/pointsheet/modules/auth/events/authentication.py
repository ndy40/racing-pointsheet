from lato import Event

from pointsheet.domain.types import EntityId


class UserAuthenticated(Event):
    user_id: EntityId
