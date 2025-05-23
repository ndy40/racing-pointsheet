from lato import Query

from modules.account import account_module
from modules.account.repository import DriverRepository
from pointsheet.domain.types import EntityId


class GetUser(Query):
    user_id: EntityId


@account_module.handler(GetUser)
def get_user(cmd: GetUser, repo: DriverRepository):
    user = repo.find_by_id(cmd.user_id)
    return user
