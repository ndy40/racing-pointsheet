from lato import Query

from modules.auth import auth_module
from modules.auth.domain import ActiveUser
from modules.auth.exceptions import InvalidUserException
from modules.auth.repository import ActiveUserRepository


class GetActiveUser(Query):
    username: str


@auth_module.handler(GetActiveUser)
def handle_get_active_user(query: GetActiveUser, repo: ActiveUserRepository):
    active_user: ActiveUser = repo.find_by_username(query.username)

    if not active_user:
        raise InvalidUserException()

    return active_user
