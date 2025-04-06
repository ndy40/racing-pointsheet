from lagom import Container

from modules.auth.repository import ActiveUserRepository, RegisterUserRepository
from pointsheet.db import get_session

container = Container()
container[ActiveUserRepository] = ActiveUserRepository(db_session_factory=get_session())
container[RegisterUserRepository] = RegisterUserRepository(
    db_session_factory=get_session()
)
