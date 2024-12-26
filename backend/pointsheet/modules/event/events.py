import logging

from lato import Event

from modules import event_module
from pointsheet.domain import EntityId

_logger = logging.getLogger(__package__)


class SeriesCreated(Event): ...


class SeriesDeleted(Event):
    id: EntityId


class SeriesUpdated(Event):
    series_id: EntityId


@event_module.handler(SeriesDeleted)
def series_deleted_listener(event: SeriesDeleted):
    _logger.info(f"Series ({event.id}) - deleted")
