from enum import Enum

from lato import Command, TransactionContext

from modules import event_module
from modules.event.commands.update_series_event import UpdateSeriesEvent
from modules.event.dependencies import container
from modules.event.domain.exceptions import SeriesNotFoundException
from modules.event.events import SeriesStarted, SeriesClosed, SeriesStatusNotStarted
from modules.event.repository import SeriesRepository
from pointsheet.domain import EntityId


class _SeriesStatus(str, Enum):
    closed = "closed"
    started = "started"
    not_started = "not_started"


class UpdateSeriesStatus(Command):
    series_id: EntityId
    status: _SeriesStatus


@event_module.handler(UpdateSeriesStatus)
def update_series_status(cmd: UpdateSeriesEvent, ctx: TransactionContext):
    repo = container[SeriesRepository]
    series = repo.find_by_id(cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    match cmd.status:
        case _SeriesStatus.started:
            series.start_series()
            ctx.publish(SeriesStarted(series_id=cmd.series_id))
        case _SeriesStatus.closed:
            series.close_series()
            ctx.publish(SeriesClosed(series_id=cmd.series_id))
        case _SeriesStatus.not_started:
            series.not_started()
            ctx.publish(SeriesStatusNotStarted(series_id=cmd.series_id))
        case _:
            raise ValueError("Invalid status")
