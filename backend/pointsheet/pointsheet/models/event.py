from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    Text,
    Table,
    Column, Boolean, inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from modules.event.domain.value_objects import SeriesStatus, ScheduleType, DriverResult
from pointsheet.domain.types import EntityId
from pointsheet.models import BaseModel, SeriesStatusType
from pointsheet.domain.types import uuid_default
from pointsheet.models.custom_types import (
    EntityIdType,
    EventStatusType,
    ScheduleTypeType,
    PydanticJsonType,
)

# Define the event_cars association table
event_cars = Table(
    "event_cars",
    BaseModel.metadata,
    Column("event_id", EntityIdType, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("car_id", Integer, ForeignKey("cars.id", ondelete="CASCADE"), primary_key=True),
)


class RaceResult(BaseModel):
    __tablename__ = "race_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "event_schedule.id", ondelete="CASCADE", name="race_results_schedule_id"
        ),
    )
    result: Mapped[List[DriverResult]] = mapped_column(
        PydanticJsonType[DriverResult](DriverResult)
    )
    mark_down: Mapped[str] = mapped_column(Text, nullable=True)
    upload_file: Mapped[str] = mapped_column(Text, nullable=True)
    schedule: Mapped["EventSchedule"] = relationship(back_populates="result")


class EventSchedule(BaseModel):
    __tablename__ = "event_schedule"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
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


class Participants(BaseModel):
    __tablename__ = "participants"
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


class Track(BaseModel):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    layout: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255))
    length: Mapped[str] = mapped_column(String(20))

    def __str__(self):
        name = self.name

        if self.layout:
            name = f"{name} ({self.layout})"

        return name


class Game(BaseModel):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    cars: Mapped[List["Car"]] = relationship("Car", back_populates="game")


class Car(BaseModel):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    game: Mapped["Game"] = relationship("Game", back_populates="cars")
    model: Mapped[str] = mapped_column(String(255))
    year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    events: Mapped[List["Event"]] = relationship(
        "Event", 
        secondary="event_cars",
        back_populates="cars"
    )

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Car):
            return False
        return self.id == other.id


class Event(BaseModel):
    __tablename__ = "events"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default()
    )
    title: Mapped[str]
    series: Mapped[Optional[EntityId]] = mapped_column(
        ForeignKey(
            "series.id",
            ondelete="cascade",
            name="series_event",
        ),
        nullable=True,
    )
    track: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    host: Mapped[EntityId] = mapped_column(EntityIdType)
    status: Mapped[Optional[str]] = mapped_column(EventStatusType)
    schedule: Mapped[Optional[List[EventSchedule]]] = relationship(
        cascade="all, delete-orphan"
    )
    drivers: Mapped[Optional[List[Participants]]] = relationship(
        Participants, cascade="all, delete-orphan"
    )
    cars: Mapped[Optional[List[Car]]] = relationship(
        "Car", 
        secondary=event_cars,
        back_populates="events"
    )
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_multi_class: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    game_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("games.id", name='event_game'), nullable=True)
    game: Mapped["Game"] = relationship("Game")

    def model_dump(self):
        cars_data = []
        if self.cars:
            for car in self.cars:
                cars_data.append({
                    "game": {
                        "id": car.game.id,
                        "name": car.game.name
                    },
                    "model": car.model,
                    "year": car.year
                })

        game_data = None
        if self.game:
            game_data = {
                "id": self.game.id,
                "name": self.game.name
            }

        return {
            "id": str(self.id),
            "title": self.title,
            "status": self.status,
            "track": self.track,
            "starts_at": self.starts_at.isoformat() if self.starts_at else None,
            "ends_at": self.ends_at.isoformat() if self.ends_at else None,
            "host": str(self.host) if self.host else None,
            "cars": cars_data,
            "game": game_data
        }

    @validates("starts_at", "ends_at", include_removes=False)
    def validate_date_formats(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value)
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        return value


class Series(BaseModel):
    __tablename__ = "series"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default()
    )
    title: Mapped[str]
    status: Mapped[Optional[str]] = mapped_column(
        SeriesStatusType, nullable=True, default=SeriesStatus.not_started
    )
    events: Mapped[Optional[List[Event]]] = relationship(cascade="all, delete")
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    cover_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def model_dump(self):
        events = [event.model_dump() for event in self.events] if self.events else []
        return {
            "id": str(self.id),
            "title": self.title,
            "status": self.status,
            "starts_at": self.starts_at.isoformat() if self.starts_at else None,
            "ends_at": self.ends_at.isoformat() if self.ends_at else None,
            "cover_image": self.cover_image,
            "description": self.description,
            "events": events,
        }

    @validates("ends_at")
    def validate_ends_at(self, key, value):
        if self.starts_at:
            # Ensure starts_at has timezone info
            starts_at = self.starts_at
            if starts_at.tzinfo is None:
                starts_at = starts_at.replace(tzinfo=timezone.utc)

            if value:
                # Ensure value has timezone info
                if value.tzinfo is None:
                    value = value.replace(tzinfo=timezone.utc)

                if starts_at > value:
                    raise ValueError("End date must be further in the future or empty")

        return value

    @validates("starts_at")
    def validate_starts_at(self, key, value):
        if value is None:
            return None

        has_changes = inspect(self).attrs.starts_at.history.has_changes()

        if not has_changes:
            return value

        # Ensure value has timezone info
        if value.tzinfo is None:
            # If value is naive, assume it's in UTC
            value = value.replace(tzinfo=timezone.utc)

        # Get current time in UTC
        now = datetime.now(timezone.utc)

        # Get beginning of today in UTC
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if value >= today:
            return value
        raise ValueError("start date must be from beginning of today or future.")
