import logging

from lato import Event

from modules.event.domain.value_objects import SeriesStatus
from pointsheet.domain import EntityId

_logger = logging.getLogger(__package__)


class SeriesCreated(Event): ...


class SeriesDeleted(Event):
    id: EntityId


class SeriesUpdated(Event):
    series_id: EntityId


class SeriesStatusUpdated(Event):
    series_id: EntityId
    status: SeriesStatus


class SeriesStarted(Event):
    series_id: EntityId


class SeriesClosed(Event):
    series_id: EntityId
