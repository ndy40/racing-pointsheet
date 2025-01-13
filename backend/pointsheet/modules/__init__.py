# Register application modules
from lato import Application

from modules.account import account_module
from modules.auth import auth_module
from modules.event import event_module

application = Application("pointsheet")
application.include_submodule(account_module)
application.include_submodule(event_module)
application.include_submodule(auth_module)
