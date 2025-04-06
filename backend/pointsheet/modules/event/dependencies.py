from lagom import Container

from modules.event.repository import EventRepository, SeriesRepository
from pointsheet.db import get_session

container = Container()
container[EventRepository] = EventRepository(db_session_factory=get_session())
container[SeriesRepository] = SeriesRepository(db_session_factory=get_session())
