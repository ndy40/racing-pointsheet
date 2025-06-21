import uuid
from datetime import datetime, timedelta

import factory
from factory import LazyFunction
from factory.alchemy import SQLAlchemyModelFactory

from modules.event.domain.value_objects import SeriesStatus, EventStatus
from pointsheet.db import Session
from pointsheet.models import Event, Series, Game
from pointsheet.models.event import Participants, Track


class SessionMixin:

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)


class EventFactory(SessionMixin, SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     session = kwargs.pop('session', None)
    #     if session:
    #         cls._meta.sqlalchemy_session = session
    #     return super()._create(model_class, *args, **kwargs)

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Event %d" % n)
    host = uuid.uuid4()
    status = EventStatus.open
    series = None
    starts_at = None
    ends_at = None
    track = None
    drivers = []
    game_id = None


class SeriesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Sequence(lambda n: "Home %d" % n)
    status = SeriesStatus.started.value
    starts_at = LazyFunction(lambda: datetime.now() + timedelta(days=1))
    ends_at = LazyFunction(lambda: datetime.now() + timedelta(days=7))
    events = []


class EventDriverFactory(SessionMixin, SQLAlchemyModelFactory):
    class Meta:
        model = Participants
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: "EventDriver %d" % n)
    event_id = None


class TrackFactory(SessionMixin, SQLAlchemyModelFactory):
    class Meta:
        model = Track
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    id: int = factory.Sequence(lambda n: n)
    name: str = factory.Sequence(lambda n: "Track %d" % n)
    layout: str = 'full'
    country: str = 'spain'
    length: str = '100'


class GameFactory(SessionMixin, SQLAlchemyModelFactory):
    class Meta:
        model = Game
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    id: int = factory.Sequence(lambda n: n)
    name: str = factory.Sequence(lambda n: "Game %d" % n)
