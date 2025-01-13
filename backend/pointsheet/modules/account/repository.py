from typing import Any, List

from modules.account.data_mappers import DriverMapper
from modules.account.domain.entity import Driver
from pointsheet.domain import EntityId
from pointsheet.models.account import Driver as DriverEntity
from pointsheet.repository import AbstractRepository, T


class DriverRepository(AbstractRepository[DriverEntity, Driver]):
    mapper_class = DriverMapper
    model_class = Driver

    def delete(self, id: Any or EntityId) -> None:
        pass

    def all(self) -> List[T]:
        pass

    def find_by_id(self, id: Any) -> T | None:
        pass
