import abc
import os
from abc import abstractmethod
from typing import Any

from itsdangerous import Serializer, URLSafeTimedSerializer

from pointsheet import config


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
    def __init__(self, max_age: int):
        super().__init__(URLSafeTimedSerializer(config.SECRET_KEY))
        self._max_age = max_age

    def serialize(self, data: Any) -> str:
        return self.serializer.dumps(data)

    def deserializer(self, data) -> Any:
        return self.serializer.loads(data, self._max_age)
