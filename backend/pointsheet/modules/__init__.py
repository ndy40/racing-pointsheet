# Register application modules
from lato import Application, TransactionContext

from modules.account import account_module
from modules.auth import auth_module
from modules.event import event_module
from pointsheet.auth import get_user_id


application = Application("pointsheet")
application.include_submodule(account_module)
application.include_submodule(event_module)
application.include_submodule(auth_module)


@application.on_enter_transaction_context
def on_enter_transaction_context(ctx: TransactionContext):
    ctx.set_dependencies(
        user_id=get_user_id(),
    )
