import abc
import os
from abc import abstractmethod
from typing import Any
from uuid import UUID

from flask import session
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from itsdangerous import BadSignature, Serializer, URLSafeTimedSerializer

from pointsheet.config import config
from pointsheet.domain.exceptions.base import PointSheetException


api_auth = HTTPTokenAuth(scheme="Bearer")
web_auth = HTTPBasicAuth()


class _AuthenticationException(PointSheetException):
    message = "Authentication failed"


@api_auth.verify_token
def verify_token(token):
    try:
        result = TimedSerializer().deserializer(token)
        return result[0]
    except BadSignature:
        raise _AuthenticationException()


@web_auth.verify_password
def verify_password(username, password):
    if session.get("is_authenticated"):
        return session.get("user_id")
    return False


def get_user_id():
    """
    Resolves and returns the authenticated user's ID from either API token or web session authentication.

    This function attempts to get the current user ID by checking both API token authentication
    and web session authentication providers. It handles different user object formats:
    - UUID objects directly representing the user ID
    - Dictionary objects containing an 'id' field

    Returns:
        UUID | None: The unique identifier of the authenticated user if found, None otherwise
    """
    for auth_provider in (api_auth, web_auth):
        if user := auth_provider.current_user():
            if isinstance(user, UUID):
                return user
            elif isinstance(user, dict):
                return user.get("id")

    return None


def generate_salt():
    return os.urandom()


class BaseSerializer(abc.ABC):
    def __init__(self, serializer: Serializer):
        self.serializer = serializer

    @abstractmethod
    def serialize(self, data: Any) -> Any: ...

    @abstractmethod
    def deserializer(self, data) -> Any: ...


class TimedSerializer(BaseSerializer):
    def __init__(self, max_age: int = None):
        super().__init__(URLSafeTimedSerializer(config.SECRET_KEY))
        self._max_age = max_age or config.AUTH_TOKEN_MAX_AGE

    def serialize(self, data: Any) -> str:
        return self.serializer.dumps(data)

    def deserializer(self, data: str) -> tuple[Any, int]:
        return self.serializer.loads(data, max_age=self._max_age, return_timestamp=True)

    def get_timestamp(self, data) -> int:
        return self.serializer.loads(
            data, max_age=self._max_age, return_timestamp=True
        )[1]
