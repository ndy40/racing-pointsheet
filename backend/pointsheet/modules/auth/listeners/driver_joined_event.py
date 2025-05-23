from modules import account_module
from modules.event.events import DriverJoinedEvent


@account_module.handler(DriverJoinedEvent)
def handle_joining_event(event: DriverJoinedEvent):
    pass
