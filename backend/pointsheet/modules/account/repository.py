from typing import Any

from sqlalchemy import select

from modules.account.data_mappers import UserMapper
from modules.account.domain.entity import User
from pointsheet.domain import EntityId
from pointsheet.models.account import User as UserEntity
from pointsheet.repository import AbstractRepository


class UserRepository(AbstractRepository[UserEntity, User]):
    mapper_class = UserMapper
    model_class = User

    def find_by_id(self, id: Any) -> User | None:
        stmt = select(UserEntity).where(UserEntity.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

    def delete(self, id: Any or EntityId) -> None:
        pass
