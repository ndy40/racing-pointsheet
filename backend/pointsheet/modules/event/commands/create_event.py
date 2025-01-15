from datetime import datetime
from typing import Optional, Self

from lato import Command
from pydantic import ValidationError, model_validator, field_validator

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from modules.event.domain.value_objects import EventStatus
from modules.event.repository import EventRepository
from pointsheet.domain import EntityId


class CreateEvent(Command):
    title: str
    host: EntityId
    track: Optional[str] = None
    status: Optional[EventStatus] = None
    rules: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

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


@event_module.handler(CreateEvent)
def create_event(cmd: CreateEvent):
    repo = container[EventRepository]
    event = Event(**cmd.model_dump())
    repo.add(event)
