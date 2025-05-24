import uuid

EntityId = uuid.UUID


class UserId:
    def __init__(self, id: EntityId):
        self._id = id

    def __str__(self):
        return self._id

    @property
    def id(self):
        return self._id


def uuid_default():
    return str(uuid.uuid4())
