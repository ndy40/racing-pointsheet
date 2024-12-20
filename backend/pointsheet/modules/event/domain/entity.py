from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from modules.event.domain.value_objects import (
    EntityId,
    EventStatus,
    ScheduleId,
    ScheduleType,
    SeriesStatus,
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
    host: EntityId
    status: Optional[EventStatus] = EventStatus.open
    rules: Optional[str] = None
    schedule: Optional[List[Schedule]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class Series(StartEndDateMixin, BaseModel):
    id: Optional[EntityId] = None
    title: str
    status: Optional[SeriesStatus] = None
    events: Optional[List[Event]] = None
