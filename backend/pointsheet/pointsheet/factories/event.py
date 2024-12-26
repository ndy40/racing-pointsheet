import uuid
from datetime import datetime, timedelta

import factory
from factory import LazyFunction
from factory.alchemy import SQLAlchemyModelFactory

from modules.event.domain.value_objects import SeriesStatus
from pointsheet.db import get_session
from pointsheet.models import Event, Series


class EventFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session_factory = get_session

    title = factory.Sequence(lambda n: "Event %d" % n)
    host = uuid.uuid4()
    status = None
    starts_at = None
    ends_at = None


class SeriesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session_factory = get_session

    title = factory.Sequence(lambda n: "Series %d" % n)
    status = SeriesStatus.started.value
    starts_at = LazyFunction(lambda: datetime.now() + timedelta(days=1))
    ends_at = LazyFunction(lambda: datetime.now() + timedelta(days=7))
    events = []
