from modules.event.domain.entity import (
    Event as EventModel,
    Schedule,
    RaceResult as RaceResultEntity,
    Track as TrackModel,
    Car as CarModel,
    Game as GameModel,
)
from modules.event.domain.entity import Series as SeriesModel, Driver as DriverModel
from pointsheet.models import (
    Event,
    Series,
    EventSchedule,
    RaceResult,
    Participants,
    Track,
    Car,
    Game,
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


class GameModelMapper(DataMapper[Game, GameModel]):
    def to_db_entity(self, instance: GameModel) -> Game:
        return Game(
            id=instance.id if hasattr(instance, 'id') else None,
            name=instance.name,
        )

    def to_domain_model(self, instance: Game) -> GameModel:
        return GameModel(
            id=instance.id,
            name=instance.name,
        )


class CarModelMapper(DataMapper[Car, CarModel]):
    def to_db_entity(self, instance: CarModel) -> Car:
        return Car(
            id=instance.id if hasattr(instance, 'id') else None,
            game_id=instance.game_id,
            model=instance.model,
            year=instance.year,
        )

    def to_domain_model(self, instance: Car) -> CarModel:
        return CarModel(
            id=instance.id,
            model=instance.model,
            year=instance.year,
            game_id=instance.game_id,
        )

class EventModelMapper(DataMapper[Event, EventModel]):
    result_mapper = ResultMapper()
    car_mapper = CarModelMapper()

    def to_db_entity(self, instance: EventModel) -> Event:
        event = Event(
            id=instance.id,
            title=instance.title,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            series=instance.series,
            host=instance.host,
            status=instance.status,
            track=instance.track,
            max_participants=instance.max_participants,
            is_multi_class=instance.is_multi_class,
            game_id=instance.game,
            schedule=[],
            drivers=[
                Participants(id=driver.id, name=driver.name, event_id=instance.id)
                for driver in instance.drivers
            ]
            if instance.drivers
            else [],
        )

        if instance.schedule:
            for schedule in instance.schedule:
                _schedule = EventSchedule(
                    type=schedule.type,
                    nbr_of_laps=schedule.nbr_of_laps or None,
                    duration=schedule.duration,
                    event_id=instance.id,
                    id=schedule.id or None,
                    result=(
                        schedule.result
                        and self.result_mapper.to_db_entity(schedule.result)
                    ),
                )
                event.schedule.append(_schedule)

        # Add cars to the event if they exist
        if instance.cars:
            event.cars = [self.car_mapper.to_db_entity(car) for car in instance.cars]
        return event

    def to_domain_model(self, instance: Event) -> EventModel:
        event = EventModel(
            title=instance.title,
            id=instance.id,
            host=instance.host,
            starts_at=instance.starts_at,
            ends_at=instance.ends_at,
            track=instance.track,
            status=instance.status,
            max_participants=instance.max_participants,
            is_multi_class=instance.is_multi_class,
            game=instance.game_id if instance.game_id else None,
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

        # Add cars to the domain model if they exist
        if instance.cars:
            for car in instance.cars:
                event.add_car(
                    self.car_mapper.to_domain_model(car)
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
            cover_image=instance.cover_image,
            description=instance.description,
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
            cover_image=instance.cover_image,
            description=instance.description,
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
