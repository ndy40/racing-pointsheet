from datetime import datetime
from typing import List, Optional, Self, Dict

from pydantic import BaseModel, model_validator

from modules.event.domain.exceptions import (
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
from pointsheet.domain import EntityId
from pointsheet.domain.entity import AggregateRoot


class StartEndDateMixin:
    starts_at: datetime
    ends_at: datetime


class Schedule(BaseModel):
    id: Optional[ScheduleId] = None
    type: ScheduleType
    nbr_of_laps: Optional[int] = None
    duration: Optional[str] = None


class Driver(BaseModel):
    id: EntityId
    name: str


class RaceResult(BaseModel):
    id: Optional[int] = None
    schedule_id: ScheduleId
    result: List[DriverResult]
    mark_down: Optional[str] = None
    upload_file: Optional[str] = None


class Event(AggregateRoot):
    title: str
    host: EntityId
    track: Optional[str] = "TBD"
    status: Optional[EventStatus] = EventStatus.open
    rules: Optional[str] = None
    schedule: Optional[List[Schedule]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    drivers: Optional[List[Driver]] = None
    results: Optional[List[RaceResult]] = []

    @model_validator(mode="after")
    def check_start_and_end_date(self) -> Self:
        if self.ends_at and not self.starts_at:
            raise ValueError("Start date much be set if end date is set")
        elif self.starts_at and self.ends_at:
            if self.ends_at < self.starts_at:
                raise ValueError("End date cannot be less than start date.")
        elif self.starts_at and not self.ends_at:
            raise ValueError("Event should have an end date")

        return self

    def add_result(self, race_result: RaceResult) -> None:
        if not self.schedule:
            raise ValueError("Cannot add result as no schedules exist.")

        # Ensure the scheduleId matches a 'race' schedule
        race_schedules = [
            schedule for schedule in self.schedule if schedule.type == ScheduleType.race
        ]

        if not any(
            schedule.id == race_result.schedule_id for schedule in race_schedules
        ):
            raise ValueError(
                f"Schedule ID {race_result.schedule_id} is not associated with a 'race' schedule."
            )

        self.results = [
            result
            for result in self.results
            if result.schedule_id != race_result.schedule_id
        ]

        # Ensure we don't exceed the number of race schedules
        if self.results:
            current_race_results = [
                result
                for result in self.results
                if any(schedule.id == result.schedule_id for schedule in race_schedules)
            ]
            if len(current_race_results) >= len(race_schedules):
                raise ValueError(
                    "Cannot add more race results than the number of 'race' schedules."
                )

        # remove RaceResult if this is an update
        self.results.append(race_result)
        self.results.sort(key=lambda r: r.schedule_id)

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
        if not self.results:
            raise ValueError("No results exist to remove.")

        self.results = [
            result for result in self.results if result.schedule_id != schedule_id
        ]
        self.results.sort(key=lambda r: r.schedule_id)


class Series(AggregateRoot):
    title: str
    status: Optional[SeriesStatus] = SeriesStatus.not_started
    events: Optional[List[Event]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

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
        try:
            old_event = next(filter(lambda x: x.id == id, self.events))
            updated_event = old_event.model_copy(update=event)
            self.events.remove(old_event)
            self.events.append(updated_event)
        except StopIteration:
            ...

        self.events.sort(key=lambda e: e.starts_at or datetime.max)

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
            if event.starts_at and not (
                self.starts_at <= event.starts_at <= self.ends_at
            ):
                is_valid = False

            if event.ends_at and not (self.ends_at >= event.ends_at >= self.starts_at):
                is_valid = False

        if not is_valid:
            raise InvalidEventDateForSeries()
