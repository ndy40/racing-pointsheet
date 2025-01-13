from enum import Enum
from typing import Optional


from pointsheet.domain.entity import AggregateRoot


class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"


class Driver(AggregateRoot):
    name: Optional[str] = None
