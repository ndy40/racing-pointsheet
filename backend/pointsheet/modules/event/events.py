from lato import Event

from modules.event.domain.value_objects import SeriesStatus
from pointsheet.domain import EntityId


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


class SeriesStatusNotStarted(Event):
    series_id: EntityId


class DriverJoinedEvent(Event):
    event_id: EntityId
    driver_id: EntityId


class DriverLeftEvent(Event):
    event_id: EntityId
    driver_id: EntityId


class EventScheduleAdded(Event):
    event_id: EntityId


class EventScheduleRemoved(Event):
    event_id: EntityId


class RaceResultUploaded(Event):
    event_id: EntityId
    schedule_id: int
