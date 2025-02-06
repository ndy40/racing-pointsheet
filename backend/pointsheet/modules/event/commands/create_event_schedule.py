from lato import Command, TransactionContext

from modules.auth.exceptions import EventNotFoundException
from modules.event import event_module
from modules.event.dependencies import container
from modules.event.repository import EventRepository
from pointsheet.domain import EntityId


class AddEventSchedule(Command):
    event_id: EntityId
    schedule_id: int
    file: str


@event_module.handler(AddEventSchedule)
def handle_add_event_schedule(cmd: AddEventSchedule, ctx: TransactionContext):
    repo = container[EventRepository]
    event = repo.find_by_id(cmd.event_id)

    if not event:
        raise EventNotFoundException()
