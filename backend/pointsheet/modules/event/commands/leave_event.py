from lato import Command, TransactionContext

from modules.event import event_module
from modules.auth.exceptions import EventNotFoundException
from modules.event.dependencies import container
from modules.event.events import DriverLeftEvent
from modules.event.repository import EventRepository
from pointsheet.domain import EntityId


class LeaveEvent(Command):
    event_id: EntityId
    driver_id: EntityId


@event_module.handler(LeaveEvent)
def handle_remove_driver_from_event(cmd: LeaveEvent, ctx: TransactionContext):
    event_repo = container[EventRepository]
    event = event_repo.find_by_id(cmd.event_id)

    if not event:
        raise EventNotFoundException()

    event.remove_driver(cmd.driver_id)
    event_repo.update(event)

    ctx.publish(DriverLeftEvent(event_id=cmd.event_id, driver_id=cmd.driver_id))
