from datetime import datetime, timedelta
from typing import Optional

from pydantic import field_validator, Field
from werkzeug.security import check_password_hash, generate_password_hash

from pointsheet.auth import TimedSerializer
from pointsheet.config import config
from .exceptions import InvalidPassword
from pointsheet.domain.entity import AggregateRoot
from .value_objects import UserRole


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
            "id": str(self.id),
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
    def hash_password(cls, password: str | bytes):
        """
        Hash the user's password and store it securely.
        """
        if isinstance(password, bytes):
            password = password.decode("utf-8")

        return generate_password_hash(password)
