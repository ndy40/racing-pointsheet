# Register application modules
import logging
import uuid
from typing import Callable

from lagom import Container
from lato import Application, TransactionContext

from pointsheet.config import config
from pointsheet.db import get_session
from .account import account_module
from .account.repository import DriverRepository, TeamRepository
from .auth import auth_module
from .auth.repository import ActiveUserRepository, RegisterUserRepository
from .dependency_provider import LagomDependencyProvider
from .event import event_module
from pointsheet.auth import get_user_id
from .event.repository import EventRepository, SeriesRepository, TrackRepository
from pointsheet.domain.types import UserId, FileStore, Config

app_container = Container()
dp = LagomDependencyProvider(app_container)


class CorrelationId(uuid.UUID):
    pass


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


application = Application("pointsheet", dependency_provider=dp)
application.include_submodule(account_module)
application.include_submodule(event_module)
application.include_submodule(auth_module)


@application.on_create_transaction_context
def on_create_transaction_context():
    txn_container = Container()
    txn_container[CorrelationId] = uuid.uuid4()

    session = next(get_session())

    # repository
    txn_container[logging.Logger] = logger
    txn_container[EventRepository] = EventRepository(session)
    txn_container[SeriesRepository] = SeriesRepository(session)
    txn_container[ActiveUserRepository] = ActiveUserRepository(session)
    txn_container[RegisterUserRepository] = RegisterUserRepository(session)
    txn_container[TrackRepository] = TrackRepository(session)
    txn_container[TeamRepository] = TeamRepository(session)
    txn_container[DriverRepository] = DriverRepository(session)

    # Create the transaction context with the dependency provider
    txn_context = TransactionContext(LagomDependencyProvider(txn_container))

    # Set the dependencies using the set_dependency method
    txn_context.set_dependency(UserId, get_user_id())
    txn_context.set_dependency(FileStore, config.file_store)
    txn_context.set_dependency(Config, config)

    return txn_context


@application.on_enter_transaction_context
def on_enter_transaction_context(ctx: TransactionContext):
    logger = ctx[logging.Logger]
    transaction_id = uuid.uuid4()
    logger = logger.getChild(f"transaction-{transaction_id}")
    ctx.dependency_provider.update(transaction_id=transaction_id, publish=ctx.publish)
    ctx.set_dependency(UserId, get_user_id())
    ctx.set_dependency(FileStore, config.file_store)
    ctx.set_dependency(Config, config)
    logger.debug("<<< Begin transaction")


@application.on_exit_transaction_context
def on_exit_transaction_context(ctx: TransactionContext, exception=None):
    logger = ctx[logging.Logger]
    logger.debug(">>> End transaction")


@application.transaction_middleware
def logging_middleware(ctx: TransactionContext, call_next: Callable):
    logger = ctx[logging.Logger]
    description = (
        f"{ctx.current_handler} -> {repr(ctx.current_action)}"
        if ctx.current_action
        else ""
    )
    logger.debug(f"Executing {description}...")
    result = call_next()
    logger.debug(f"Finished executing {description}")
    return result
