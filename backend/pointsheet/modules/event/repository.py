from typing import Any, List

from sqlalchemy import select

from pointsheet.models import Event
from pointsheet.repository import AbstractRepository, DataMapper

from .domain.entity import Event as EventModel


class EventModelMapper(DataMapper[Event, EventModel]):
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


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> Event | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

    def all(self) -> List[EventModel]:
        stmt = select(Event).order_by(Event.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]
