from lato import Command, TransactionContext

from modules.auth.exceptions import EventNotFoundException
from modules.event import event_module
from modules.event.dependencies import container
from modules.event.events import EventScheduleRemoved
from modules.event.repository import EventRepository
from pointsheet.domain import EntityId


class RemoveSchedule(Command):
    event_id: EntityId
    schedule_id: int


@event_module.handler(RemoveSchedule)
def handle_remove_event(cmd: RemoveSchedule, ctx: TransactionContext):
    event_repo = container[EventRepository]
    event = event_repo.find_by_id(cmd.event_id)

    if not event:
        raise EventNotFoundException()

    event.remove_schedule(cmd.schedule_id)
    event_repo.update(event)
    ctx.publish(EventScheduleRemoved(event_id=cmd.event_id))
