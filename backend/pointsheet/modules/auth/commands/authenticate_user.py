from lato import Command, TransactionContext

from modules import event_module
from modules.auth.dependencies import container
from modules.auth.exceptions import InvalidUserException
from modules.auth.repository import ActiveUserRepository


class AuthUser(Command):
    username: str
    password: str


@event_module.handler(AuthUser)
def handle_authenticate_user(cmd: AuthUser, ctx: TransactionContext):
    repo = container[ActiveUserRepository]
    active_user = repo.find_by_username(cmd.username)

    if not active_user:
        raise InvalidUserException()

    active_user.verify_password(cmd.password)
    active_user.login()
    repo.update(active_user)
