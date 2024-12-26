from lato import Command, TransactionContext

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.entity import Event
from pointsheet.domain import EntityId
from modules.event.events import SeriesUpdated
from modules.event.domain.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository


class CreateEventForSeries(Command):
    series_id: EntityId
    event: Event


@event_module.handler(CreateEventForSeries)
def create_series_event(cmd: CreateEventForSeries, ctx: TransactionContext):
    repo: SeriesRepository = container[SeriesRepository]
    series = repo.find_by_id(id=cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    series.add_event(cmd.event)
    repo.update(series)
    ctx.publish(SeriesUpdated(series_id=cmd.series_id))
