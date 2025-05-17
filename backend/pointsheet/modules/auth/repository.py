from typing import Any, List

from sqlalchemy import select

from modules.auth.data_mapper import ActiveUserMapper, RegisterUserMapper
from modules.auth.domain import ActiveUser, RegisteredUser
from pointsheet.domain import EntityId
from pointsheet.models import User
from pointsheet.repository import AbstractRepository, T


class ActiveUserRepository(AbstractRepository[User, ActiveUser]):
    mapper_class = ActiveUserMapper
    model_class = ActiveUser

    def find_user_by_token(self, token) -> ActiveUser | None:
        stmt = select(User).where(User.auth_token == token)
        active_user = self._session.execute(stmt).scalar()

        if active_user:
            return self._map_to_model(active_user)
        return None

    def find_by_username(self, username: str) -> ActiveUser:
        stmt = select(User).where(User.username == username)
        active_user = self._session.execute(stmt).scalar()

        if active_user:
            return self._map_to_model(active_user)
        return None

    def delete(self, id: Any or EntityId) -> None:
        pass

    def all(self) -> List[T]:
        pass

    def find_by_id(self, id: Any) -> T | None:
        pass


class RegisterUserRepository(AbstractRepository[User, RegisteredUser]):
    mapper_class = RegisterUserMapper
    model_class = RegisteredUser

    def create_user(self, user: RegisteredUser):
        entity = self._map_to_entity(user)
        self._session.add(entity)
        self._session.commit()

    def delete(self, id: Any or EntityId) -> None:
        pass

    def all(self) -> List[T]:
        pass

    def find_by_id(self, id: Any) -> T | None:
        pass
