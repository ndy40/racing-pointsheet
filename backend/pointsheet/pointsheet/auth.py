import abc
import os
from abc import abstractmethod
from typing import Any

from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadSignature, Serializer, URLSafeTimedSerializer

from pointsheet.config import config
from pointsheet.domain.exceptions.base import PointSheetException

auth = HTTPTokenAuth(scheme="Bearer")


class _AuthenticationException(PointSheetException):
    message = "Authentication failed"


@auth.verify_token
def verify_token(token):
    try:
        result = TimedSerializer().deserializer(token)
        return result[0]
    except BadSignature:
        raise _AuthenticationException()


def get_user_id():
    if user := auth.current_user():
        return user["id"]


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
