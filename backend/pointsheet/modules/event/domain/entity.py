from datetime import datetime
from typing import List, Optional, Self

from pydantic import BaseModel, model_validator

from modules.event.domain.exceptions import (
    InvalidEventDateForSeries,
    SeriesAlreadyClosed,
)
from modules.event.domain.value_objects import (
    EventStatus,
    ScheduleId,
    ScheduleType,
    SeriesStatus,
)
from pointsheet.domain import EntityId
from pointsheet.domain.entity import AggregateRoot


class StartEndDateMixin:
    starts_at: datetime
    ends_at: datetime


class Schedule(BaseModel):
    id: Optional[ScheduleId] = None
    type: ScheduleType
    nbr_of_laps: int
    duration: str


class Event(AggregateRoot):
    id: Optional[EntityId] = None
    title: str
    host: EntityId
    status: Optional[EventStatus] = EventStatus.open
    rules: Optional[str] = None
    schedule: Optional[List[Schedule]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

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


class Series(AggregateRoot):
    title: str
    status: Optional[SeriesStatus] = SeriesStatus.not_started
    events: Optional[List[Event]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    def add_event(self, event: Event):
        self._check_event_is_within_date(event)

        if not self.events:
            self.events = []
        # check if event is already added.
        try:
            item: Event = next(filter(lambda x: x.id == event.id, self.events))
            updated_item = item.model_copy(update=event.model_dump(exclude_none=True))
            self.events.remove(item)
            event = updated_item
        except StopIteration:
            ...
        finally:
            self.events.append(event)

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

        if self.starts_at and self.ends_at:
            if event.starts_at and not (
                self.starts_at <= event.starts_at <= self.ends_at
            ):
                is_valid = False

            if event.ends_at and not (self.ends_at >= event.ends_at >= self.starts_at):
                is_valid = False

        if not is_valid:
            raise InvalidEventDateForSeries()
