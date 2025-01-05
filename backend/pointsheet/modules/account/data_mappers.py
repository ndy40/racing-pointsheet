from pointsheet.models.account import User
from pointsheet.repository import DataMapper

from .domain.entity import User as UserModel


class UserMapper(DataMapper[User, UserModel]):
    def to_db_entity(self, instance: UserModel) -> User:
        return User(
            id=instance.id,
            username=instance.username,
            password=instance.password,
            role=instance.role,
            is_active=instance.is_active,
            last_login=instance.last_login,
            auth_token=instance.auth_token,
            auth_expires_in=instance.auth_expires_in,
        )

    def to_domain_model(self, instance: User) -> UserModel:
        return UserModel(
            id=instance.id,
            username=instance.username,
            password=instance.password,
            role=instance.role,
            is_active=instance.is_active,
            last_login=instance.last_login,
            auth_token=instance.auth_token,
            auth_expires_in=instance.auth_expires_in,
        )
