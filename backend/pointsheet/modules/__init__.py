# Register application modules
from lato import Application, TransactionContext

from pointsheet.config import config
from .account import account_module
from .auth import auth_module
from .event import event_module
from pointsheet.auth import get_user_id


application = Application("pointsheet")
application.include_submodule(account_module)
application.include_submodule(event_module)
application.include_submodule(auth_module)


@application.on_enter_transaction_context
def on_enter_transaction_context(ctx: TransactionContext):
    ctx.set_dependencies(
        user_id=get_user_id(), file_store=config.file_store, config=config
    )
