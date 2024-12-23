from lato import Command, TransactionContext

from modules import event_module
from modules.event.dependencies import container
from modules.event.domain.value_objects import EntityId
from modules.event.events import SeriesUpdated
from modules.event.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository


class DeleteSeriesEvent(Command):
    series_id: EntityId
    event_id: EntityId


@event_module.handler(DeleteSeriesEvent)
def handle_delete_series_event(cmd: DeleteSeriesEvent, ctx: TransactionContext):
    repository: SeriesRepository = container[SeriesRepository]
    series = repository.find_by_id(cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    series.remove_event(cmd.event_id)
    repository.update(series)
    ctx.publish(SeriesUpdated(series_id=cmd.series_id))
