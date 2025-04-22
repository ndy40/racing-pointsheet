# Register application modules
import uuid

from lagom import Container
from lato import Application, TransactionContext

from pointsheet.config import config
from pointsheet.db import Session
from .account import account_module
from .account.repository import DriverRepository
from .auth import auth_module
from .auth.repository import ActiveUserRepository, RegisterUserRepository
from .dependency_provider import LagomDependencyProvider
from .event import event_module
from pointsheet.auth import get_user_id
from .event.repository import EventRepository, SeriesRepository, TrackRepository

app_container = Container()
app_container[Session] = Session()
dp = LagomDependencyProvider(app_container)


class CorrelationId(uuid.UUID):
    pass


application = Application("pointsheet", dependency_provider=dp)
application.include_submodule(account_module)
application.include_submodule(event_module)
application.include_submodule(auth_module)


@application.on_create_transaction_context
def on_create_transaction_context():
    session = application.dependency_provider.get_dependency(Session)
    txn_container = Container()
    txn_container[CorrelationId] = uuid.uuid4()

    # repository
    txn_container[EventRepository] = EventRepository(session)
    txn_container[SeriesRepository] = SeriesRepository(session)
    txn_container[ActiveUserRepository] = ActiveUserRepository(session)
    txn_container[RegisterUserRepository] = RegisterUserRepository(session)
    txn_container[TrackRepository] = TrackRepository(session)
    txn_container[DriverRepository] = DriverRepository(session)

    return TransactionContext(
        LagomDependencyProvider(txn_container),
        user_id=get_user_id(),
        file_store=config.file_store,
        config=config,
    )


#
# @application.on_enter_transaction_context
# def on_enter_transaction_context(ctx: TransactionContext):
#     ctx.set_dependencies(
#         user_id=get_user_id(), file_store=config.file_store, config=config
#     )
