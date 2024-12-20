from typing import Any

from sqlalchemy import select

from pointsheet.models import Event
from pointsheet.repository import AbstractRepository, DataMapper, T

from .domain.entity import Event as EventModel


class EventModelMapper(DataMapper[Event, EventModel]):
    def to_entity(self, instance: Event) -> EventModel:
        return EventModel(
            # id=instance.id,
            # title=instance.title,
            # starts_at=instance.starts_at,
            # ends_at=instance.ends_at
        )

    def to_model(self, instance: EventModel) -> Event:
        return Event(
            title=instance.title,
            id=instance.id if instance.id else None,
            host=instance.host,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
        )


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> T | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_entity(result)
