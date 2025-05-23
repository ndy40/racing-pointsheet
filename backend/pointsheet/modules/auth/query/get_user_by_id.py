from lato import Query
from uuid import UUID

from modules.auth import auth_module
from modules.auth.domain import ActiveUser
from modules.auth.exceptions import InvalidUserException
from modules.auth.repository import ActiveUserRepository


class GetUserById(Query):
    user_id: UUID


@auth_module.handler(GetUserById)
def handle_get_user_by_id(query: GetUserById, repo: ActiveUserRepository):
    active_user: ActiveUser = repo.find_by_id(query.user_id)

    if not active_user:
        raise InvalidUserException()

    return active_user
