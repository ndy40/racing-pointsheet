import uuid

from factory import LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from pointsheet.db import Session
from pointsheet.models.account import Driver


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Driver
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: "User %d" % n)
