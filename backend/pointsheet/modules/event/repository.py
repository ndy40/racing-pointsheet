from pointsheet.models import Event
from pointsheet.repository import AbstractRepository, DataMapper

from .domain.entity import Event as EventModel


class EventModelMapper(DataMapper[Event, EventModel]):
    def to_entity(self, instance: Event) -> EventModel:
        pass

    def from_model(self, instance: EventModel) -> Event:
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
