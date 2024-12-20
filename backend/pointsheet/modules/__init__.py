# Register application modules
from lato import Application

from .event import event_module

application = Application("pointsheet")
application.include_submodule(event_module)
