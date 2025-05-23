from logging import Logger
from typing import Optional

from lato import Command, TransactionContext

from modules.auth import auth_module
from modules.auth.domain import UserRole
from modules.auth.events.user_registered import UserRegistered, UserRegisteredWithTeam
from modules.auth.exceptions import UserAlreadyExists
from modules.auth.repository import ActiveUserRepository, RegisterUserRepository
from pydantic import Field, field_validator
from werkzeug.security import generate_password_hash


class RegisterUser(Command):
    password: str
    username: str = Field(max_length=50)
    role: Optional[UserRole] = Field(default=UserRole.driver)
    team: Optional[str] = None

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, password: str):
        """
        Hash the user's password and store it securely.
        """
        if isinstance(password, str):
            return generate_password_hash(password)

        raise ValueError("Invalid password provided")

    @field_validator("team")
    @classmethod
    def validate_team(cls, team: Optional[str], info):
        if team is not None and info.data.get("role") != UserRole.admin:
            raise ValueError("Only admin users can provide team name")
        return team


@auth_module.handler(RegisterUser)
def handle_register_user(
    cmd: RegisterUser,
    repo: RegisterUserRepository,
    active_repo: ActiveUserRepository,
    logging: Logger,
    ctx: TransactionContext,
):
    active_user = active_repo.find_by_username(username=cmd.username)

    if active_user:
        raise UserAlreadyExists()

    logging.debug(f"Registering user {cmd.id}")
    repo.create_user(cmd)
    logging.debug(f"User {cmd.id} registered")

    event = (
        UserRegisteredWithTeam(
            user_id=cmd.id, team_name=cmd.team, username=cmd.username
        )
        if cmd.team
        else UserRegistered(user_id=cmd.id, username=cmd.username)
    )

    logging.debug(f"Publishing event {repr(event)}")
    ctx.publish(event)
