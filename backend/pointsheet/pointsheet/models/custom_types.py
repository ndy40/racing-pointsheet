from typing import Optional, Any

from sqlalchemy import TypeDecorator, Dialect, CHAR, String
from sqlalchemy.sql.type_api import _T

from event.domain.value_objects import SeriesStatus, EntityId


class BaseCustomTypes(TypeDecorator):
    ...


class EntityIdType(BaseCustomTypes):
    impl = CHAR

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value:
            return str(value)

        return None

    def process_result_value(self, value: Optional[Any], dialect: Dialect) -> Optional[_T]:
        if value:
            return EntityId(value)

        return None


class SeriesStatusType(BaseCustomTypes):
    impl = String

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value not in SeriesStatus.__members__.values():
            raise ValueError(f'Invalid value for SeriesStatus: {value}')
        return value

    def process_result_value(self, value: Optional[Any], dialect: Dialect) -> Optional[_T]:
        return SeriesStatus(value)

    def __repr__(self):
        return 'SeriesStatusType()'