import uuid
from datetime import datetime, timedelta

import factory
from factory import LazyFunction
from factory.alchemy import SQLAlchemyModelFactory

from modules.event.domain.value_objects import SeriesStatus, EventStatus
from pointsheet.db import Session
from pointsheet.models import Event, Series
from pointsheet.models.event import Participants, Track


class EventFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Event %d" % n)
    host = uuid.uuid4()
    status = EventStatus.open
    series = None
    starts_at = None
    ends_at = None
    track = None
    drivers = []


class SeriesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session_factory = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Home %d" % n)
    status = SeriesStatus.started.value
    starts_at = LazyFunction(lambda: datetime.now() + timedelta(days=1))
    ends_at = LazyFunction(lambda: datetime.now() + timedelta(days=7))
    events = []


class EventDriverFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Participants
        sqlalchemy_session_factory = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: "EventDriver %d" % n)
    event_id = None


class TrackFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Track
        sqlalchemy_session_factory = Session
    id: int = factory.Sequence(lambda n: n)
    name: str = factory.Sequence(lambda n: "Track %d" % n)
    layout: str = 'full'
    country: str = 'spain'
    length: str = '100'
