from typing import Any, Optional

from sqlalchemy import CHAR, Dialect, String, TypeDecorator
from sqlalchemy.sql.type_api import _T

from modules.event.domain.value_objects import EntityId, EventStatus, SeriesStatus


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
