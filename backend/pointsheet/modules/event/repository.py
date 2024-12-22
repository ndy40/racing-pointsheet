from typing import Any, List

from sqlalchemy import select

from pointsheet.models import Event, Series
from pointsheet.repository import AbstractRepository, DataMapper

from .domain.entity import Event as EventModel
from .domain.entity import Series as SeriesModel


class _EventModelMapper(DataMapper[Event, EventModel]):
    def to_db_entity(self, instance: EventModel) -> Event:
        return Event(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            host=instance.host,
        )

    def to_domain_model(self, instance: Event) -> EventModel:
        return EventModel(
            title=instance.title,
            id=instance.id,
            host=instance.host,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
        )


class _SeriesModelMapper(DataMapper[Series, SeriesModel]):
    def to_db_entity(self, instance: SeriesModel) -> Series:
        return Series(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            status=instance.status,
        )

    def to_domain_model(self, instance: Series) -> SeriesModel:
        return SeriesModel(
            id=instance.id,
            title=instance.title,
            ends_at=instance.ends_at,
            starts_at=instance.starts_at,
            status=instance.status,
        )


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = _EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> EventModel | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

    def all(self) -> List[EventModel]:
        stmt = select(Event).order_by(Event.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]


class SeriesRepository(AbstractRepository[Series, SeriesModel]):
    mapper_class = _SeriesModelMapper
    model_class = SeriesModel

    def all(self) -> List[SeriesModel]:
        stmt = select(Series).order_by(Series.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: Any) -> SeriesModel | None:
        stmt = select(Series).where(Series.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
