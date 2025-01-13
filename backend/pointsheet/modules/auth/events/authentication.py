from lato import Event

from pointsheet.domain import EntityId


class UserAuthenticated(Event):
    user_id: EntityId
