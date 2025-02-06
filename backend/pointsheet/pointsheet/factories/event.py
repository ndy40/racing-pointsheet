import uuid
from datetime import datetime, timedelta

import factory
from factory import LazyFunction
from factory.alchemy import SQLAlchemyModelFactory

from modules.event.domain.value_objects import SeriesStatus, EventStatus
from pointsheet.db import get_session
from pointsheet.models import Event, Series
from pointsheet.models.event import EventDriver


class EventFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session_factory = get_session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Event %d" % n)
    host = uuid.uuid4()
    status = EventStatus.open
    starts_at = None
    ends_at = None
    track = None
    drivers = []


class SeriesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session_factory = get_session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Series %d" % n)
    status = SeriesStatus.started.value
    starts_at = LazyFunction(lambda: datetime.now() + timedelta(days=1))
    ends_at = LazyFunction(lambda: datetime.now() + timedelta(days=7))
    events = []


class EventDriverFactory(SQLAlchemyModelFactory):
    class Meta:
        model = EventDriver
        sqlalchemy_session_factory = get_session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: "EventDriver %d" % n)
    event_id = None
