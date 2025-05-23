import json
from typing import Any, Optional, TypeVar, Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import CHAR, Dialect, String, TypeDecorator, JSON
from sqlalchemy.sql.type_api import _T

from modules.auth.value_objects import UserRole
from modules.event.domain.value_objects import (
    EventStatus,
    SeriesStatus,
    ScheduleType,
)
from pointsheet.domain.entity import EntityId


class BaseCustomTypes(TypeDecorator): ...


class EntityIdType(BaseCustomTypes):
    impl = CHAR
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value:
            return str(value)

        return None

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_T]:
        if value:
            return EntityId(value)

        return None


class SeriesStatusType(BaseCustomTypes):
    impl = String

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value and value not in SeriesStatus.__members__.values():
            raise TypeError(f"Invalid value for SeriesStatus: {value}")
        return value

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_T]:
        if not value:
            return value

        return SeriesStatus(value)

    def __repr__(self):
        return "SeriesStatusType()"


class EventStatusType(BaseCustomTypes):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value and value not in EventStatus.__members__.values():
            raise TypeError(f"Invalid value for EventStatus: {value}")

        return value

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_T]:
        if not value:
            return value

        return EventStatus(value)

    def __repr__(self):
        return "EventStatusType()"


class UserRoleType(BaseCustomTypes):
    impl = String

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value and value not in UserRole.__members__.values():
            raise TypeError("Invalid user role")
        return value

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_T]:
        if not value:
            return value

        return UserRole(value)

    def __repr__(self):
        return "EventStatusType()"


class ScheduleTypeType(BaseCustomTypes):
    impl = String

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value and value not in ScheduleType.__members__.values():
            raise TypeError(f"Invalid value for ScheduleType: {value}")
        return value

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[_T]:
        if not value:
            return value

        return ScheduleType(value)

    def __repr__(self):
        return "ScheduleTypeType()"


T = TypeVar("T", bound=BaseModel)


class PydanticJsonType[T](BaseCustomTypes):
    impl = JSON

    def __init__(self, cls: Type[T], *args, **kwargs):
        self.cls = cls
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Optional[list[T] | T], dialect: Dialect) -> Any:
        if not value:
            return value

        if isinstance(value, list):
            return [item.model_dump() for item in value]

        return value.model_dump()

    def process_result_value(
        self, value: Optional[Any], dialect: Dialect
    ) -> Optional[Any]:
        if not value:
            return value

        if isinstance(value, list):
            return [
                self.cls(**json.loads(item)) if isinstance(item, str) else item
                for item in value
            ]

        return self.cls(**json.loads(value))


class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return UUID(value) if not isinstance(value, UUID) else value
