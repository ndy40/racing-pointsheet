from pointsheet.models import User
from pointsheet.repository import DataMapper

from .domain.entity import User as UserModel


class UserMapper(DataMapper[User, UserModel]):
    def to_db_entity(self, instance: UserModel) -> User:
        return User(
            id=instance.id,
            name=instance.name,
        )

    def to_domain_model(self, instance: User) -> UserModel:
        return UserModel(
            id=instance.id,
            name=instance.name,
        )
