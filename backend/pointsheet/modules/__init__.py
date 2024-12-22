# Register application modules
from lato import Application

from modules.event import event_module

application = Application("pointsheet")
application.include_submodule(event_module)
