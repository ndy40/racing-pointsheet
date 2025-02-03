from lagom import Container

from .repository import DriverRepository
from pointsheet.db import get_session

container = Container()
container[DriverRepository] = DriverRepository(db_session=get_session())
