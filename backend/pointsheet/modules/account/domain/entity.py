from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from modules.account.domain.exceptions import AlreadySignedUpException
from pointsheet.domain import EntityId
from pointsheet.domain.entity import AggregateRoot


class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"


class RaceEvent(BaseModel):
    event_id: EntityId
    title: str
    status: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    track: Optional[str] = None


class Driver(AggregateRoot):
    name: Optional[str] = None
    events: Optional[List[RaceEvent]] = None

    def join_event(self, event: RaceEvent):
        if any(
            existing_event.event_id == event.event_id for existing_event in self.events
        ):
            raise AlreadySignedUpException(
                f"Driver is already signed up for event {event.event_id}."
            )
        self.events.append(event)
