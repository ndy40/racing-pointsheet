from datetime import datetime
from typing import Optional

from lato import Command

from modules.event.domain.value_objects import EventStatus
from pointsheet.domain import EntityId


class CreateEvent(Command):
    title: str
    host: EntityId
    track: Optional[str] = None
    status: Optional[EventStatus] = EventStatus.open
    rules: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
