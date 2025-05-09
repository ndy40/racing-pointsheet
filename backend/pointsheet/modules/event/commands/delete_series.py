from lato import Command, TransactionContext

from modules.event import event_module
from pointsheet.domain import EntityId
from modules.event.events import SeriesDeleted
from modules.event.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository


class DeleteSeries(Command):
    id: EntityId


@event_module.handler(DeleteSeries)
def delete_series(cmd: DeleteSeries, ctx: TransactionContext, repo: SeriesRepository):
    series = repo.find_by_id(id=cmd.id)

    if not series:
        raise SeriesNotFoundException()

    # do some business rules checks here
    repo.delete(series.id)

    # publish event here
    ctx.publish(SeriesDeleted(id=cmd.id))
