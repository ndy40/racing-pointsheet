from typing import Any

from sqlalchemy import select

from modules.account.data_mappers import DriverMapper, TeamMapper
from modules.account.domain.entity import Driver, Team
from pointsheet.domain import EntityId
from pointsheet.models.account import Driver as DriverEntity, Team as TeamEntity
from pointsheet.repository import AbstractRepository


class UserRepository(AbstractRepository[DriverEntity, Driver]):
    mapper_class = DriverMapper
    model_class = Driver

    def find_by_id(self, id: Any) -> Driver | None:
        stmt = select(DriverEntity).where(DriverEntity.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

        return None

    def delete(self, id: Any or EntityId) -> None:
        pass


class TeamRepository(AbstractRepository[TeamEntity, Team]):
    mapper_class = TeamMapper
    model_class = Team

    def find_by_id(self, id: Any) -> Team | None:
        stmt = select(TeamEntity).where(TeamEntity.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

        return None

    def delete(self, id: Any or EntityId) -> None:
        pass
