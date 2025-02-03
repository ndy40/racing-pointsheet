from typing import Any

from sqlalchemy import select

from modules.account.data_mappers import DriverMapper
from modules.account.domain.entity import Driver
from pointsheet.domain import EntityId
from pointsheet.models.account import Driver as DriverEntity
from pointsheet.repository import AbstractRepository


class DriverRepository(AbstractRepository[DriverEntity, Driver]):
    mapper_class = DriverMapper
    model_class = Driver

    def find_by_id(self, id: Any) -> Driver | None:
        stmt = select(DriverEntity).where(DriverEntity.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

    def delete(self, id: Any or EntityId) -> None:
        pass
