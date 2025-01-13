import importlib


from lato import ApplicationModule

account_module = ApplicationModule("account_module")

importlib.import_module("modules.account.events")
