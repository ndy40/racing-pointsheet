import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from event.domain.value_objects import (
    SeriesStatus,
    EventStatus,
    ScheduleId,
    ScheduleType,
    EntityId,
)


class StartEndDateMixin:
    starts_at: datetime
    ends_at: datetime


class Schedule(BaseModel):
    id: Optional[ScheduleId] = None
    type: ScheduleType
    nbr_of_laps: int
    duration: str


class Event(StartEndDateMixin, BaseModel):
    id: Optional[EntityId] = None
    title: str
    host: uuid.UUID
    status: Optional[EventStatus] = EventStatus.open
    rules: Optional[str] = None
    schedule: Optional[List[Schedule]] = None


class Series(StartEndDateMixin, BaseModel):
    id: Optional[EntityId] = None
    title: str
    status: Optional[SeriesStatus] = None
    events: Optional[List[Event]] = None
