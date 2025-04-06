from lato import Command, TransactionContext

from modules.event import event_module
from modules.event.domain.entity import Event
from pointsheet.domain import EntityId
from modules.event.events import SeriesUpdated
from modules.event.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository


class CreateEventForSeries(Command):
    series_id: EntityId
    event: Event


@event_module.handler(CreateEventForSeries)
def create_series_event(
    cmd: CreateEventForSeries, ctx: TransactionContext, repo: SeriesRepository
):
    series = repo.find_by_id(id=cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    series.add_event(cmd.event)
    repo.update(series)
    ctx.publish(SeriesUpdated(series_id=cmd.series_id))
