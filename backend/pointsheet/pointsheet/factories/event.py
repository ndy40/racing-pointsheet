import uuid

import factory
from factory.alchemy import SQLAlchemyModelFactory

from modules.event.domain.value_objects import SeriesStatus
from pointsheet.db import get_session
from pointsheet.models import Event, Series


class SeriesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session_factory = get_session

    title = factory.Sequence(lambda n: "Series %d" % n)
    status = SeriesStatus.started.value


class EventFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session_factory = get_session

    title = factory.Sequence(lambda n: "Event %d" % n)
    host = uuid.uuid4()
