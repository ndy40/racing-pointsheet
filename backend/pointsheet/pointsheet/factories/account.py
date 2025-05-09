import uuid

from factory import LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from pointsheet.db import get_db_session
from pointsheet.models.account import Driver


class DriverFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Driver
        sqlalchemy_session_factory = get_db_session
        sqlalchemy_session_persistence = "commit"

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: "Driver %d" % n)
