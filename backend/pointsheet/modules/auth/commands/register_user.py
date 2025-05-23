from typing import Optional

from lato import Command, TransactionContext
from modules.auth import auth_module
from modules.auth.domain import UserRole
from modules.auth.events.user_registered import UserRegistered
from modules.auth.exceptions import UserAlreadyExists
from modules.auth.repository import ActiveUserRepository, RegisterUserRepository
from pydantic import Field, field_validator
from werkzeug.security import generate_password_hash


class RegisterUser(Command):
    password: str
    username: str = Field(max_length=50)
    role: Optional[UserRole] = Field(default=UserRole.driver)

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, password: str):
        """
        Hash the user's password and store it securely.
        """
        if isinstance(password, str):
            return generate_password_hash(password)

        raise ValueError("Invalid password provided")


@auth_module.handler(RegisterUser)
def handle_register_user(
    cmd: RegisterUser,
    ctx: TransactionContext,
    repo: RegisterUserRepository,
    active_repo: ActiveUserRepository,
):
    active_user = active_repo.find_by_username(username=cmd.username)

    if active_user:
        raise UserAlreadyExists()

    repo.create_user(cmd)
    ctx.publish(UserRegistered(user_id=cmd.id))
