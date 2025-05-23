from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, PositiveInt, field_serializer, NonNegativeInt

from pointsheet.domain.types import EntityId

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


class DriverResult(BaseModel):
    driver_id: EntityId
    driver: str
    position: PositiveInt
    total: Optional[str] = None
    best_lap: Optional[str] = None
    penalties: Optional[int] = 0
    fl_points: Optional[int] = 0
    points: Optional[int] = 0
    total_points: Optional[NonNegativeInt] = 0

    @field_serializer("driver_id")
    def serialize_driver_id(self, driver_id: EntityId):
        return str(driver_id)


class Result(BaseModel):
    position: NonNegativeInt
    driver: str
    driver_id: Optional[EntityId] = None
    best_lap: Optional[str] = None
    race: Optional[str] = None
    penalties: Optional[float] = None
    total: Optional[str] = None


class ListOfResults(BaseModel):
    results: List[Result]
