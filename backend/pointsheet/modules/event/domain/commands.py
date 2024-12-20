from typing import Optional

from lato import Command

from modules.event.domain.value_objects import SeriesStatus


class CreateSeries(Command):
    title: str
    description: str
    status: Optional[SeriesStatus] = None
