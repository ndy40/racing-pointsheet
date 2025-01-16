import abc
import os
from abc import abstractmethod
from typing import Any

from itsdangerous import Serializer, URLSafeTimedSerializer

from pointsheet.config import config


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
        return self.serializer.dumps(data).encode("utf-8")

    def deserializer(self, data: str) -> tuple[Any, int]:
        return self.serializer.loads(data.encode("utf-8"), return_timestamp=True)

    def get_timestamp(self, data) -> int:
        return self.serializer.loads(data, return_timestamp=True)[1]
