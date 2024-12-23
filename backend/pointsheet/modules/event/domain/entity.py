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


class Series(BaseModel):
    id: Optional[EntityId] = None
    title: str
    status: Optional[SeriesStatus] = None
    events: Optional[List[Event]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    def add_event(self, event: Event):
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
