from flask import current_app
from lato import Command, TransactionContext


from modules.event import event_module
from modules.event.exceptions import DriverNotFound
from modules.event.events import DriverJoinedEvent
from modules.event.repository import EventRepository
from pointsheet.domain.types import EntityId


class JoinEvent(Command):
    event_id: EntityId
    driver_id: EntityId


@event_module.handler(JoinEvent)
def handle_join_event(
    cmd: JoinEvent, ctx: TransactionContext, event_repo: EventRepository
):
    from modules.account.queries.get_user import GetUser

    driver = current_app.application.execute(GetUser(user_id=cmd.driver_id))

    if not driver:
        raise DriverNotFound()

    event = event_repo.find_by_id(cmd.event_id)
    event.add_driver(driver)
    event_repo.update(event)
    ctx.publish(DriverJoinedEvent(event_id=cmd.event_id, driver_id=cmd.driver_id))
