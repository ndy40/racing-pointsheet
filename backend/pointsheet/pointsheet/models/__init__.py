from sqlalchemy.orm import DeclarativeBase
from .custom_types import (
    EntityId,
    EntityIdType,
    SeriesStatusType,
    SeriesStatus,
)
from .event import Event, Series


__all__ = [
    Event,
    Series,
    EntityId,
    EntityIdType,
    SeriesStatusType,
    SeriesStatus,
]


class BaseModel(DeclarativeBase):
    pass
