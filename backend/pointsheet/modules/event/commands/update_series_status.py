from enum import Enum

from lato import Command, TransactionContext

from modules.event import event_module
from modules.event.commands.update_series_event import UpdateSeriesEvent
from modules.event.exceptions import SeriesNotFoundException
from modules.event.events import SeriesStarted, SeriesClosed, SeriesStatusNotStarted
from modules.event.repository import SeriesRepository
from pointsheet.domain.types import EntityId


class _SeriesStatus(str, Enum):
    closed = "closed"
    started = "started"
    not_started = "not_started"


class UpdateSeriesStatus(Command):
    series_id: EntityId
    status: _SeriesStatus


@event_module.handler(UpdateSeriesStatus)
def update_series_status(
    cmd: UpdateSeriesEvent, ctx: TransactionContext, repo: SeriesRepository
):
    series = repo.find_by_id(cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    published_event = None

    match cmd.status:
        case _SeriesStatus.started:
            series.start_series()
            published_event = SeriesStarted(series_id=cmd.series_id)
        case _SeriesStatus.closed:
            series.close_series()
            published_event =  SeriesClosed(series_id=cmd.series_id)
        case _SeriesStatus.not_started:
            series.not_started()
        case _:
            raise ValueError("Invalid status")

    repo.update(series)

    if published_event:
        ctx.publish(published_event)