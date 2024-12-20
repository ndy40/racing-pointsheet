from lato import ApplicationModule

from .handlers import command_handlers, query_handlers

event_module = ApplicationModule("event_module")


__all__ = ["command_handlers", "query_handlers"]
