from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from pointsheet.domain.entity import AggregateRoot


class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"


class User(AggregateRoot):
    username: str
    password: str = Field(exclude=True)
    auth_token: str
    auth_expires_in: Optional[datetime] = None
    last_login: Optional[datetime] = None
    role: Optional[UserRole] = UserRole.driver
    is_active: Optional[bool] = True

    def generate_token(self) -> str:
        """
        Generates and saves token to the `auth_token` field and returns said token.
        sets expiry date.
        :return:
        """
        pass
