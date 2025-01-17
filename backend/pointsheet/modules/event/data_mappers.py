from modules.event.domain.entity import Event as EventModel, Schedule
from modules.event.domain.entity import Series as SeriesModel, Driver as DriverModel
from pointsheet.models import Event, Series, EventSchedule
from pointsheet.models.event import Driver
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
            schedule=[
                EventSchedule(
                    type=schedule.type,
                    nbr_of_laps=schedule.nbr_of_laps,
                    duration=schedule.duration,
                    id=schedule.id,
                )
                for schedule in instance.schedule
            ]
            if instance.schedule
            else [],
            drivers=[
                Driver(id=driver.id, name=driver.name) for driver in instance.drivers
            ]
            if instance.drivers
            else [],
        )

    def to_domain_model(self, instance: Event) -> EventModel:
        event = EventModel(
            title=instance.title,
            id=instance.id,
            host=instance.host,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            status=instance.status,
            drivers=[
                DriverModel(id=instance.id, name=instance.name)
                for instance.drivers in instance.drivers
            ],
        )

        if instance.schedule:
            for schedule in instance.schedule:
                event.add_schedule(
                    Schedule(
                        type=schedule.type,
                        nbr_of_laps=schedule.nbr_of_laps,
                        duration=schedule.duration,
                        id=schedule.id,
                    )
                )

        return event


class SeriesModelMapper(DataMapper[Series, SeriesModel]):
    event_mapper = EventModelMapper()

    def to_db_entity(self, instance: SeriesModel) -> Series:
        return Series(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            status=instance.status,
            events=[self.event_mapper.to_db_entity(event) for event in instance.events]
            if instance.events
            else [],
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
            ]
            if instance.events
            else [],
        )
