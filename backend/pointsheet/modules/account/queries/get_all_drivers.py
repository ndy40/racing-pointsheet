from lato import Query

from modules.account import account_module
from modules.account.repository import DriverRepository


class GetAllDrivers(Query):
    pass


@account_module.handler(GetAllDrivers)
def get_all_drivers(cmd: GetAllDrivers, repo: DriverRepository):
    drivers = repo.all()
    return drivers