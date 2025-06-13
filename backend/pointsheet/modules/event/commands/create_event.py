from datetime import datetime
from typing import Optional, Self, List

from flask import current_app
from lato import Command
from pyarrow.tests.util import random_seed
from pydantic import ValidationError, model_validator, field_validator

from modules.event import event_module
from modules.event.domain.entity import Event, Car
from modules.event.domain.value_objects import EventStatus
from modules.event.exceptions import HostNotFound, SeriesNotFoundException, NoCarFound
from modules.event.repository import EventRepository, CarRepository, TrackRepository
from pointsheet.domain.types import EntityId


class CreateEvent(Command):
    title: str
    host: EntityId
    track: int
    status: Optional[EventStatus] = None
    rules: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    cars: Optional[List[int]] = None
    is_multi_class: Optional[bool] = None
    max_participants: Optional[int] = None
    series: Optional[EntityId] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_value(cls, value):
        if value not in (None, EventStatus.open):
            raise ValidationError(
                "The status field can only be None or EventStatus.open."
            )
        return value

    @model_validator(mode="after")
    def validate_status(self) -> Self:
        if self.starts_at and self.ends_at:
            delta = self.ends_at - self.starts_at
            if delta.days > 31:
                raise ValueError(
                    "The end date cannot be more than 31 days away from the start date."
                )
        return self

    @field_validator("host", mode="after")
    @classmethod
    def validate_host(cls, value):
        from modules.account.queries.get_user import GetUser
        from flask import current_app
        if value:
            host = current_app.application.execute(GetUser(user_id=value))
            if not host:
                raise HostNotFound("Host not found")
        return value

    @field_validator("series", mode="after")
    @classmethod
    def validate_series(cls, value):
        if value:
            from modules.event.queries.get_series_by_id import GetSeriesById
            from flask import current_app
            series = current_app.application.execute(GetSeriesById(id=value))
            if not series:
                raise SeriesNotFoundException("Series not found")
        return value
    
    

@event_module.handler(CreateEvent)
def create_event(cmd: CreateEvent, repo: EventRepository, car_repo: CarRepository, track_repo: TrackRepository):
    event = Event(**cmd.model_dump(exclude={"cars", "track"}))

    if cmd.cars:
        cars = car_repo.find_by_ids(cmd.cars)
        if not cars:
            raise NoCarFound()

        event.cars = cars if cars else []

    if cmd.track:
        track = track_repo.find_by_id(cmd.track)
        event.track = track.id

    repo.add(event)
