from datetime import datetime
from typing import Optional

from lato import Command

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Series
from modules.event.domain.value_objects import SeriesStatus
from modules.event.repository import SeriesRepository


class CreateSeries(Command):
    title: str
    description: Optional[str] = None
    status: Optional[SeriesStatus] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


@event_module.handler(CreateSeries)
def create_series(cmd: CreateSeries):
    repo: SeriesRepository = container[SeriesRepository]
    model = Series(**cmd.model_dump())
    repo.add(model)
