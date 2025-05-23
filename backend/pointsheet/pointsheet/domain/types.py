import uuid
from typing import NewType

EntityId = uuid.UUID

# Define new types for dependency injection
UserId = NewType("UserId", str)
FileStore = NewType("FileStore", str)
Config = NewType("Config", object)


def uuid_default():
    return str(uuid.uuid4())
