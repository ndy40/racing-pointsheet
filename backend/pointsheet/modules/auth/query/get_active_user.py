from lato import Query

from modules import auth_module
from modules.auth.dependencies import container
from modules.auth.domain import ActiveUser
from modules.auth.exceptions import InvalidUserException
from modules.auth.repository import ActiveUserRepository


class GetActiveUser(Query):
    username: str


@auth_module.handler(GetActiveUser)
def handle_get_active_user(query: GetActiveUser):
    repo = container[ActiveUserRepository]
    active_user: ActiveUser = repo.find_by_username(query.username)

    if not active_user:
        raise InvalidUserException()

    return active_user
