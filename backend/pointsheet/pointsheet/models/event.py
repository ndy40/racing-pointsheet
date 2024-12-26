import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from modules.event.domain.value_objects import SeriesStatus
from pointsheet.domain.entity import EntityId
from pointsheet.models import BaseModel, SeriesStatusType
from pointsheet.models.custom_types import EntityIdType, EventStatusType


def uuid_default():
    return str(uuid.uuid4())


class Event(BaseModel):
    __tablename__ = "events"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    title: Mapped[str]
    series: Mapped[Optional[str]] = mapped_column(
        ForeignKey(
            "series.id",
            ondelete="cascade",
            name="series_event",
        ),
        nullable=True,
    )
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    host: Mapped[str] = mapped_column(EntityIdType)
    status: Mapped[Optional[str]] = mapped_column(EventStatusType)


class Series(BaseModel):
    __tablename__ = "series"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    title: Mapped[str]
    status: Mapped[Optional[str]] = mapped_column(
        SeriesStatusType, nullable=True, default=SeriesStatus.not_started
    )
    events: Mapped[List[Event]] = relationship(cascade="all, delete")
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    @validates("ends_at")
    def validate_ends_at(self, key, value):
        if self.starts_at and (not value or self.starts_at > value):
            raise ValueError("End date must be further in the future or empty")
        return value

    @validates("starts_at")
    def validate_starts_at(self, key, value):
        if value:
            if value > datetime.now():
                return value
            raise ValueError("start date much be in the future. ")
