from typing import Any, List

from modules.account.data_mappers import UserMapper
from modules.account.domain.entity import User
from pointsheet.domain import EntityId
from pointsheet.models.account import User as UserEntity
from pointsheet.repository import AbstractRepository, T


class UserRepository(AbstractRepository[UserEntity, User]):
    mapper_class = UserMapper
    model_class = User

    def delete(self, id: Any or EntityId) -> None:
        pass

    def all(self) -> List[T]:
        pass

    def find_by_id(self, id: Any) -> T | None:
        pass
