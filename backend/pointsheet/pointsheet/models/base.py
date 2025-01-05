import uuid

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


def uuid_default():
    return str(uuid.uuid4())
