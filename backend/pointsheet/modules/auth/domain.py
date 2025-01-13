from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import field_validator, Field
from werkzeug.security import check_password_hash, generate_password_hash

from modules.auth.auth import TimedSerializer
from pointsheet.config import config
from .exceptions import InvalidPassword
from pointsheet.domain.entity import AggregateRoot


class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"


class ActiveUser(AggregateRoot):
    username: str
    password: str = Field(repr=False, exclude=True)
    auth_token: Optional[str] = None
    auth_expires_in: Optional[datetime] = None

    def verify_password(self, password: str):
        """
        Verify the provided password against the stored hashed password.
        """
        if not check_password_hash(self.password, password):
            # Handle invalid password scenario
            raise InvalidPassword("Invalid password provided")

    def login(self):
        payload = {
            "username": self.username,
        }
        serializer = TimedSerializer()
        self.auth_token = serializer.serialize(payload)
        sign_timestamp = serializer.get_timestamp(self.auth_token)
        self.auth_expires_in = sign_timestamp + timedelta(
            minutes=config.AUTH_TOKEN_MAX_AGE
        )
        return self.auth_token


class RegisteredUser(AggregateRoot):
    username: str
    password: str = Field(repr=False)
    role: Optional[UserRole] = UserRole.driver

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, password: str):
        """
        Hash the user's password and store it securely.
        """
        if isinstance(password, str):
            return generate_password_hash(password)

        raise ValueError("Invalid password provided")
