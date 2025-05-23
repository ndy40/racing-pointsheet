from modules.event.domain.entity import (
    Event as EventModel,
    Schedule,
    RaceResult as RaceResultEntity,
    Track as TrackModel,
)
from modules.event.domain.entity import Series as SeriesModel, Driver as DriverModel
from pointsheet.models import (
    Event,
    Series,
    EventSchedule,
    RaceResult,
    EventDriver,
    Track,
)
from pointsheet.repository import DataMapper


class ResultMapper(DataMapper[RaceResult, RaceResultEntity]):
    def to_db_entity(self, instance: RaceResultEntity) -> RaceResult:
        return RaceResult(
            id=instance.id,
            schedule_id=instance.schedule_id,
            upload_file=instance.upload_file,
            mark_down=instance.mark_down,
            result=instance.result,
        )

    def to_domain_model(self, instance: RaceResult) -> RaceResultEntity:
        return RaceResultEntity(
            id=instance.id,
            schedule_id=instance.schedule_id,
            upload_file=instance.upload_file,
            mark_down=instance.mark_down,
            result=instance.result,
        )


class EventModelMapper(DataMapper[Event, EventModel]):
    result_mapper = ResultMapper()

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
                    result=(
                        schedule.result
                        and self.result_mapper.to_db_entity(schedule.result)
                    ),
                )
                for schedule in instance.schedule
            ]
            if instance.schedule
            else [],
            drivers=[
                EventDriver(id=driver.id, name=driver.name, event_id=instance.id)
                for driver in instance.drivers
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
                DriverModel(id=driver.id, name=driver.name)
                for driver in instance.drivers
            ]
            if instance.drivers
            else None,
        )

        if instance.schedule:
            for schedule in instance.schedule:
                event.add_schedule(
                    Schedule(
                        type=schedule.type,
                        nbr_of_laps=schedule.nbr_of_laps,
                        duration=schedule.duration,
                        id=schedule.id,
                        result=(
                            schedule.result
                            and self.result_mapper.to_domain_model(schedule.result)
                        ),
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


class TrackModelMapper(DataMapper[Track, TrackModel]):
    def to_db_entity(self, instance: TrackModel) -> Track:
        return Track(
            id=instance.id,
            name=instance.name,
            country=instance.country,
            layout=instance.layout,
            length=instance.length,
        )

    def to_domain_model(self, instance: Track) -> TrackModel:
        return TrackModel(
            id=instance.id,
            name=instance.name,
            layout=instance.layout,
            country=instance.country,
            length=instance.length,
        )
