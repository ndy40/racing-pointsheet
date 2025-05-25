from datetime import datetime, timezone
from typing import Optional

from lato import Command, TransactionContext

from modules.event import event_module
from modules.event.events import SeriesUpdated
from modules.event.exceptions import SeriesNotFoundException
from modules.event.repository import SeriesRepository
from pointsheet.domain.types import EntityId


class UpdateSeries(Command):
    series_id: EntityId
    title: Optional[str] = None
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    cover_image: Optional[str] = None


@event_module.handler(UpdateSeries)
def update_series(cmd: UpdateSeries, ctx: TransactionContext, repo: SeriesRepository):
    series = repo.find_by_id(cmd.series_id)

    if not series:
        raise SeriesNotFoundException()

    # Convert datetime objects to UTC timezone if they have no timezone info
    data = cmd.model_dump(exclude={"series_id"}, exclude_none=True)

    if data.get("starts_at") and data["starts_at"].tzinfo is None:
        data["starts_at"] = data["starts_at"].replace(tzinfo=timezone.utc)

    if data.get("ends_at") and data["ends_at"].tzinfo is None:
        data["ends_at"] = data["ends_at"].replace(tzinfo=timezone.utc)

    # Update the series with the new data
    updated_series = series.model_copy(update=data)
    repo.update(updated_series)

    # Publish event
    ctx.publish(SeriesUpdated(series_id=cmd.series_id))
