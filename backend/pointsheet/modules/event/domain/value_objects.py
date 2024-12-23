import uuid
from enum import Enum

EntityId = uuid.UUID
ScheduleId = int


class SeriesStatus(str, Enum):
    started = "started"
    closed = "closed"
    not_started = "not_started"


class EventStatus(str, Enum):
    open = "open"
    closed = "closed"
    in_progress = "in_progress"


class ScheduleType(str, Enum):
    practice = "practice"
    qualification = "qualification"
    race = "race"
