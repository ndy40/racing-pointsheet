from typing import Optional

from lato import Command, TransactionContext
from pydantic import BaseModel

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.value_objects import EventStatus
from pointsheet.domain import EntityId
from modules.event.events import SeriesUpdated
from modules.event.domain.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository


class UpdateEventModel(BaseModel):
    id: EntityId
    title: Optional[str] = None
    host: Optional[EntityId] = None
    status: Optional[EventStatus] = None


class UpdateSeriesEvent(Command):
    series_id: EntityId
    event: UpdateEventModel


@event_module.handler(UpdateSeriesEvent)
def update_series_event(cmd: UpdateSeriesEvent, ctx: TransactionContext):
    repo: SeriesRepository = container[SeriesRepository]
    series = repo.find_by_id(cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    series.update_event(
        cmd.event.id, cmd.event.model_dump(exclude_none=True, exclude_unset=True)
    )
    repo.update(series)
    ctx.publish(SeriesUpdated(series_id=cmd.series_id))
