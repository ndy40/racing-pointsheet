from lato import Event

from pointsheet.domain import EntityId


class UserRegistered(Event):
    user_id: EntityId
