from datetime import datetime, timezone
from typing import List, Optional, Self, Dict

from numpy import integer
from pydantic import BaseModel, model_validator, computed_field

from modules.event.exceptions import (
    InvalidEventDateForSeries,
    SeriesAlreadyClosed,
    DriverAlreadySingedUp,
)
from modules.event.domain.value_objects import (
    EventStatus,
    ScheduleId,
    ScheduleType,
    SeriesStatus,
    DriverResult,
)
from pointsheet.domain.entity import AggregateRoot
from pointsheet.domain.types import EntityId


class StartEndDateMixin:
    starts_at: datetime
    ends_at: datetime


class RaceResult(BaseModel):
    id: Optional[int] = None
    schedule_id: ScheduleId
    result: List[DriverResult]
    mark_down: Optional[str] = None
    upload_file: Optional[str] = None

    def add_result(self, *driver_results: DriverResult) -> None:
        """
        Adds one or more DriverResults to the race result list.

        :param driver_results: One or more DriverResult instances.
        :raises TypeError: If any input is not a DriverResult instance.
        """

        for driver_result in driver_results:
            if not isinstance(driver_result, DriverResult):
                raise TypeError(
                    "All provided results must be instances of DriverResult."
                )
            self.result.append(driver_result)


class Schedule(BaseModel):
    id: Optional[ScheduleId] = None
    type: ScheduleType
    nbr_of_laps: Optional[int] = None
    duration: Optional[str] = None
    result: Optional[RaceResult] = None

    def add_result(self, race_result: RaceResult) -> None:
        """
        Assigns a RaceResult to this schedule's result field.

        :param race_result: A RaceResult instance.
        :raises TypeError: If the provided result is not a RaceResult instance.
        """
        if not isinstance(race_result, RaceResult):
            raise TypeError("The provided result must be an instance of RaceResult.")
        self.result = race_result


class Driver(BaseModel):
    id: EntityId
    name: str


class Track(BaseModel):
    id: int
    name: str
    layout: str
    country: str
    length: str


class Game(BaseModel):
    id: int
    name: str


class Car(BaseModel):
    id: int
    model: str
    year: Optional[str] = None


class Event(AggregateRoot):
    title: str
    host: EntityId
    track: Optional[str] = "-"
    status: Optional[EventStatus] = EventStatus.open
    series: Optional[EntityId] = None
    rules: Optional[str] = None
    schedule: Optional[List[Schedule]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    drivers: Optional[List[Driver]] = None
    cars: Optional[List[Car]] = None

    @model_validator(mode="after")
    def check_start_and_end_date(self) -> Self:
        if self.ends_at and not self.starts_at:
            raise ValueError("Start date much be set if end date is set")
        elif self.starts_at and self.ends_at:
            # Ensure dates have timezone info
            starts_at = self.starts_at
            ends_at = self.ends_at

            if starts_at.tzinfo is None:
                starts_at = starts_at.replace(tzinfo=timezone.utc)

            if ends_at.tzinfo is None:
                ends_at = ends_at.replace(tzinfo=timezone.utc)

            if ends_at < starts_at:
                raise ValueError("End date cannot be less than start date.")
        elif self.starts_at and not self.ends_at:
            raise ValueError("Event should have an end date")

        return self

    def add_result(self, race_result: RaceResult) -> None:
        """
        Assigns a RaceResult to the correct Schedule's result field.

        :param race_result: A RaceResult instance.
        :raises ValueError: If the result is invalid, or the schedule is not found.
        """
        if not isinstance(race_result, RaceResult):
            raise TypeError("The provided result must be an instance of RaceResult.")

        schedule = next(
            (
                schedule
                for schedule in (self.schedule or [])
                if schedule.id == race_result.schedule_id
            ),
            None,
        )
        if schedule is None:
            raise ValueError("Cannot add result as schedule does not exist")

        schedule.result = race_result

    def add_driver(self, driver: Driver) -> None:
        if not self.drivers:
            self.drivers = []

        if not any(existing_driver.id == driver.id for existing_driver in self.drivers):
            self.drivers.append(driver)
            return

        raise DriverAlreadySingedUp()

    def remove_driver(self, driver_id: EntityId) -> None:
        if self.drivers:
            self.drivers = [driver for driver in self.drivers if driver.id != driver_id]

    def find_driver_by_id_or_name(self, identifier: str | EntityId) -> Optional[Driver]:
        """
        Find a driver by ID or name. Returns None if no driver is found.

        :param identifier: The ID or name of the driver to find.
        :return: The Driver instance if found, otherwise None.
        """
        if not self.drivers:
            return None

        return next(
            (
                driver
                for driver in self.drivers
                if driver.id == identifier
                or (
                    isinstance(identifier, str)
                    and driver.name.lower() == identifier.lower()
                )
            ),
            None,
        )

    def add_schedule(self, schedule: Schedule) -> None:
        if not self.schedule:
            self.schedule = []

        if schedule.type in {ScheduleType.practice, ScheduleType.qualification}:
            if any(s.type == schedule.type for s in self.schedule):
                raise ValueError(
                    f"Cannot add multiple schedules of type '{schedule.type.value}'."
                )

        self.schedule.append(schedule)
        self.schedule.sort(
            key=lambda s: {"practice": 0, "qualification": 1, "race": 2}.get(
                s.type.value, 3
            )
        )

    def remove_schedule(self, schedule_id: int) -> None:
        if self.schedule:
            self.schedule = [
                schedule for schedule in self.schedule if schedule.id != schedule_id
            ]
            self.schedule.sort(
                key=lambda s: {"practice": 0, "qualification": 1, "race": 2}.get(
                    s.type.value, 999
                )
            )

    def remove_result(self, schedule_id: ScheduleId) -> None:
        """Removes the result associated with the given schedule_id from the respective schedule."""
        if not self.schedule:
            raise ValueError("No schedules exist to remove a result from.")

        # Find the schedule with the matching schedule_id
        schedule = next((s for s in self.schedule if s.id == schedule_id), None)
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found.")

        # Remove the result from the found schedule
        schedule.result = None

    def is_participating(self, driver_id: EntityId) -> bool:
        return self.find_driver_by_id_or_name(driver_id) is not None

    def add_car(self, car: Car) -> None:
        if not self.cars:
            self.cars = []

        self.cars.append(car)

    def remove_car(self, car_model: str) -> None:
        if self.cars:
            self.cars = [car for car in self.cars if car.model != car_model]


class Series(AggregateRoot):
    title: str
    status: Optional[SeriesStatus] = SeriesStatus.not_started
    events: Optional[List[Event]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None

    @computed_field
    @property
    def event_count(self) -> int:
        return len(self.events) if self.events else 0

    def add_event(self, event: Event):
        self._check_event_is_within_date(event)

        if self.events is None:
            self.events = []

        try:
            item: Event = next(filter(lambda x: x.id == event.id, self.events))
            updated_item = item.model_copy(update=event.model_dump(exclude_none=True))
            self.events.remove(item)
            event = updated_item
        except StopIteration:
            ...

        self.events.append(event)
        self.events.sort(key=lambda e: e.starts_at or datetime.max)

    def update_event(self, id: EntityId, event: Dict):
        if not self.events:
            self.events = []
            return

        try:
            old_event = next(filter(lambda x: x.id == id, self.events))
            updated_event = old_event.model_copy(update=event)
            self.events.remove(old_event)
            self.events.append(updated_event)
            self.events.sort(key=lambda e: e.starts_at or datetime.max)
        except StopIteration:
            pass

    def remove_event(self, event_id: EntityId):
        try:
            event: Event = next(filter(lambda x: x.id == event_id, self.events))
            self.events.remove(event)
        except StopIteration:
            ...

    def start_series(self):
        if self.status == SeriesStatus.closed:
            raise SeriesAlreadyClosed()

        self.status = SeriesStatus.started

    def close_series(self):
        self.status = SeriesStatus.closed

    def _check_event_is_within_date(self, event: Event) -> None:
        is_valid = True

        if not event:
            raise ValueError("Event cannot be None")

        if self.starts_at and self.ends_at:
            # Ensure series dates have timezone info
            series_starts_at = self.starts_at
            series_ends_at = self.ends_at

            if series_starts_at.tzinfo is None:
                series_starts_at = series_starts_at.replace(tzinfo=timezone.utc)

            if series_ends_at.tzinfo is None:
                series_ends_at = series_ends_at.replace(tzinfo=timezone.utc)

            if event.starts_at:
                # Ensure event start date has timezone info
                event_starts_at = event.starts_at
                if event_starts_at.tzinfo is None:
                    event_starts_at = event_starts_at.replace(tzinfo=timezone.utc)

                if not (series_starts_at <= event_starts_at <= series_ends_at):
                    is_valid = False

            if event.ends_at:
                # Ensure event end date has timezone info
                event_ends_at = event.ends_at
                if event_ends_at.tzinfo is None:
                    event_ends_at = event_ends_at.replace(tzinfo=timezone.utc)

                if not (series_ends_at >= event_ends_at >= series_starts_at):
                    is_valid = False

        if not is_valid:
            raise InvalidEventDateForSeries()
