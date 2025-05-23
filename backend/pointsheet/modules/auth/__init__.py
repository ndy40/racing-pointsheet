import importlib

from lato import ApplicationModule

auth_module = ApplicationModule("auth_module")

importlib.import_module("modules.auth.commands")
importlib.import_module("modules.auth.query")
importlib.import_module("modules.auth.events")
