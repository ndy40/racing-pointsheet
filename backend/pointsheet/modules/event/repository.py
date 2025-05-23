from datetime import datetime
from typing import Any, List

from lato import Query
from sqlalchemy import select, or_

from pointsheet.models import Event, Series, Participants, Track
from pointsheet.repository import AbstractRepository

from .data_mappers import EventModelMapper, SeriesModelMapper, TrackModelMapper
from .domain.entity import Event as EventModel
from .domain.entity import Series as SeriesModel
from .domain.entity import Track as TrackModel
from pointsheet.domain import EntityId
from .domain.value_objects import EventStatus


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> EventModel | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
        return None

    def all(self) -> List[EventModel]:
        stmt = select(Event).order_by(Event.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Event.id, id)
        self._session.delete(entity_to_delete)
        self._session.commit()

    def get_recent_event_by_user(self, query: Query):
        driver_search = {"id": str(query.driver_id)}

        stmt = (
            select(Event)
            .where(Event.drivers.contains([driver_search]))
            .order_by(Event.starts_at.desc())
            .limit(1)
        )
        result = self._session.execute(stmt).scalar()
        return self._map_to_model(result) if result else None

    def get_available_events(self, query: Query = None):
        stmt = (
            select(Event)
            .where(Event.starts_at > datetime.now(), Event.status == EventStatus.open)
            .order_by(Event.starts_at)
        )

        if query.user_id:
            stmt = stmt.outerjoin(Participants).where(
                or_(Participants.id != query.user_id, Participants.id.is_(None))
            )

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def get_ongoing_events(self, query: Query):
        stmt = (
            select(Event)
            .where(Event.status.in_([EventStatus.in_progress, EventStatus.open]))
            .order_by(Event.starts_at)
        )

        if query.user_id:
            stmt = stmt.join(Participants).where(Participants.id == str(query.user_id))

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]


class SeriesRepository(AbstractRepository[Series, SeriesModel]):
    mapper_class = SeriesModelMapper
    model_class = SeriesModel

    def all(self, criteria: Query) -> List[SeriesModel]:
        stmt = select(Series).order_by(Series.id)

        if value := getattr(criteria, "status"):
            stmt = stmt.where(Series.status == value.value)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: Any) -> SeriesModel | None:
        result = self._session.get(Series, id)

        if result:
            return self._map_to_model(result)
        return None

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Series, id)
        self._session.delete(entity_to_delete)
        self._session.commit()


class TrackRepository(AbstractRepository[Track, TrackModel]):
    mapper_class = TrackModelMapper
    model_class = TrackModel

    def all(self) -> List[TrackModel]:
        stmt = select(Track).order_by(Track.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: Any or EntityId) -> None:
        pass
