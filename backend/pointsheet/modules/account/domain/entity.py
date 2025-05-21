from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from modules.account.domain.exceptions import AlreadySignedUpException
from pointsheet.domain import EntityId
from pointsheet.domain.entity import AggregateRoot


class RaceEvent(BaseModel):
    event_id: EntityId
    title: str
    status: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    track: Optional[str] = None


class User(AggregateRoot):
    name: Optional[str] = None
    events: Optional[List[RaceEvent]] = None

    def join_event(self, event: RaceEvent):
        if any(
            existing_event.event_id == event.event_id for existing_event in self.events
        ):
            raise AlreadySignedUpException(
                f"User is already signed up for event {event.event_id}."
            )
        self.events.append(event)
