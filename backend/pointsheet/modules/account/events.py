from modules.account import account_module
from modules.account.domain.entity import Driver
from modules.account.repository import DriverRepository
from modules.auth.events.user_registered import UserRegistered


@account_module.handler(UserRegistered)
def on_registered_user(event: UserRegistered, repo: DriverRepository):
    driver = Driver(id=event.user_id)
    repo.add(driver)
