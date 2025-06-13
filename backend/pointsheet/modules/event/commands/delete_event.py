from lato import Command, TransactionContext

from modules.event import event_module
from modules.event.repository import EventRepository
from modules.auth.exceptions import EventNotFoundException
from pointsheet.domain.types import EntityId
from modules.event.events import EventDeleted


class DeleteEvent(Command):
    event_id: EntityId


@event_module.handler(DeleteEvent)
def handle_delete_event(cmd: DeleteEvent, ctx: TransactionContext, repo: EventRepository):
    event = repo.find_by_id(cmd.event_id)
    if not event:
        raise EventNotFoundException()

    repo.delete(cmd.event_id)
    ctx.publish(EventDeleted(event_id=cmd.event_id))
    return None