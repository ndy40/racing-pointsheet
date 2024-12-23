from modules.event.domain.entity import Event as EventModel
from modules.event.domain.entity import Series as SeriesModel
from pointsheet.models import Event, Series
from pointsheet.repository import DataMapper


class EventModelMapper(DataMapper[Event, EventModel]):
    def to_db_entity(self, instance: EventModel) -> Event:
        return Event(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            host=instance.host,
            status=instance.status,
        )

    def to_domain_model(self, instance: Event) -> EventModel:
        return EventModel(
            title=instance.title,
            id=instance.id,
            host=instance.host,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            status=instance.status,
        )


class SeriesModelMapper(DataMapper[Series, SeriesModel]):
    event_mapper = EventModelMapper()

    def to_db_entity(self, instance: SeriesModel) -> Series:
        return Series(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            status=instance.status,
            events=[self.event_mapper.to_db_entity(event) for event in instance.events],
        )

    def to_domain_model(self, instance: Series) -> SeriesModel:
        return SeriesModel(
            id=instance.id,
            title=instance.title,
            ends_at=instance.ends_at,
            starts_at=instance.starts_at,
            status=instance.status,
            events=[
                self.event_mapper.to_domain_model(event) for event in instance.events
            ],
        )
