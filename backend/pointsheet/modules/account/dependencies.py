from lagom import Container

from .repository import DriverRepository
from pointsheet.db import get_db_session

container = Container()
container[DriverRepository] = DriverRepository(db_session_factory=get_db_session)
