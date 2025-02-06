from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from modules.event.domain.value_objects import SeriesStatus, ScheduleType, DriverResult
from pointsheet.domain.entity import EntityId
from pointsheet.models import BaseModel, SeriesStatusType, DriverResultType
from pointsheet.models.base import uuid_default
from pointsheet.models.custom_types import (
    EntityIdType,
    EventStatusType,
    ScheduleTypeType,
    PydanticJsonType,
)


class RaceResult(BaseModel):
    __tablename__ = "race_results"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    schedule_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "event_schedule.id", ondelete="CASCADE", name="race_results_schedule_id"
        ),
    )
    result: Mapped[List[DriverResult]] = mapped_column(
        PydanticJsonType[List[DriverResultType]]
    )
    mark_down: Mapped[str] = mapped_column(Text, nullable=True)
    upload_file: Mapped[str] = mapped_column(Text, nullable=True)
    schedule: Mapped["EventSchedule"] = relationship(back_populates="result")


class EventSchedule(BaseModel):
    __tablename__ = "event_schedule"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=True
    )
    type: Mapped[ScheduleType] = mapped_column(ScheduleTypeType)
    nbr_of_laps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    event_id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        ForeignKey("events.id", ondelete="CASCADE", name="event_schedule_event"),
        nullable=False,
    )
    result: Mapped[Optional[RaceResult]] = relationship(
        back_populates="schedule", cascade="all, delete-orphan"
    )


class Driver(BaseModel):
    __tablename__ = "event_drivers"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default()
    )
    name: Mapped[str] = mapped_column(String(255))
    event_id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        ForeignKey("events.id", ondelete="CASCADE", name="drivers_event"),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("id", "event_id", name="unique_driver_event"),)


class Event(BaseModel):
    __tablename__ = "events"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default()
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
    track: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    host: Mapped[EntityId] = mapped_column(EntityIdType)
    status: Mapped[Optional[str]] = mapped_column(EventStatusType)
    schedule: Mapped[Optional[List[EventSchedule]]] = relationship(
        cascade="all, delete-orphan"
    )
    drivers: Mapped[Optional[List[Driver]]] = relationship(
        Driver, cascade="delete-orphan, all"
    )


class Series(BaseModel):
    __tablename__ = "series"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    title: Mapped[str]
    status: Mapped[Optional[str]] = mapped_column(
        SeriesStatusType, nullable=True, default=SeriesStatus.not_started
    )
    events: Mapped[Optional[List[Event]]] = relationship(cascade="all, delete")
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
