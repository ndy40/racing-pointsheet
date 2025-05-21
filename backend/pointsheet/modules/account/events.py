from modules.account import account_module
from modules.account.domain.entity import User
from modules.account.repository import UserRepository
from modules.auth.events.user_registered import UserRegistered


@account_module.handler(UserRegistered)
def on_registered_user(event: UserRegistered, repo: UserRepository):
    user = User(id=event.user_id)
    repo.add(user)
