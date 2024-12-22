import importlib

from lato import ApplicationModule

event_module = ApplicationModule("event_module")
importlib.import_module("modules.event.commands")
importlib.import_module("modules.event.queries")
