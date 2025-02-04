from modules import account_module
from modules.event.events import DriverLeftEvent


@account_module.handler(DriverLeftEvent)
def handle_leaving_event(event: DriverLeftEvent): ...
