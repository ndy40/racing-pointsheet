from datetime import datetime
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
    model = Series(**cmd.model_dump())
    repo.add(model)
