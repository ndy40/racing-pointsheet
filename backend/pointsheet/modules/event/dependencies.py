from lagom import Container

from modules.event.repository import EventRepository
from pointsheet.db import get_session

container = Container()
container[EventRepository] = EventRepository(db_session=get_session())
