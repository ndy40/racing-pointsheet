from datetime import datetime, timezone
from typing import Optional

from lato import Command

from modules.event import event_module
from modules.event.domain.entity import Series
from modules.event.repository import SeriesRepository


class CreateSeries(Command):
    title: str
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


@event_module.handler(CreateSeries)
def create_series(cmd: CreateSeries, repo: SeriesRepository):
    # Convert datetime objects to UTC timezone if they have no timezone info
    data = cmd.model_dump()

    if data.get("starts_at") and data["starts_at"].tzinfo is None:
        data["starts_at"] = data["starts_at"].replace(tzinfo=timezone.utc)

    if data.get("ends_at") and data["ends_at"].tzinfo is None:
        data["ends_at"] = data["ends_at"].replace(tzinfo=timezone.utc)

    model = Series(**data)
    repo.add(model)
