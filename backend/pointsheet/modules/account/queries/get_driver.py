from lato import Query

from modules.account import account_module
from modules.account.dependencies import container
from modules.account.repository import DriverRepository
from pointsheet.domain import EntityId


class GetDriver(Query):
    driver_id: EntityId


@account_module.handler(GetDriver)
def get_driver(cmd: GetDriver):
    repo = container[DriverRepository]
    driver = repo.find_by_id(cmd.driver_id)

    return driver
