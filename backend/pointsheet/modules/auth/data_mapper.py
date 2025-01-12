from modules.auth.domain import ActiveUser, RegisteredUser
from pointsheet.repository import DataMapper
from pointsheet.models import User


class ActiveUserMapper(DataMapper[User, ActiveUser]):
    def to_db_entity(self, instance: ActiveUser) -> User:
        return User(
            id=instance.id,
            username=instance.username,
            password=instance.password,
            auth_token=instance.auth_token,
            auth_expires_in=instance.auth_expires_in,
        )

    def to_domain_model(self, instance: User) -> ActiveUser:
        return ActiveUser(
            id=instance.id,
            username=instance.username,
            password=instance.password,
            auth_token=instance.auth_token,
            auth_expires_in=instance.auth_expires_in,
        )


class RegisterUserMapper(DataMapper[User, RegisteredUser]):
    def to_db_entity(self, instance: RegisteredUser) -> User:
        return User(
            id=instance.id, username=instance.username, password=instance.password
        )

    def to_domain_model(self, instance: User) -> RegisteredUser:
        raise NotImplementedError
