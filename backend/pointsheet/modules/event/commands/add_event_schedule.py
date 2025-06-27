from typing import Self

from lato import Command, TransactionContext
from pydantic import model_validator, NonNegativeInt
from typing_extensions import Optional

from modules.auth.exceptions import EventNotFoundException
from modules.event import event_module
from modules.event.domain.entity import Schedule
from modules.event.domain.value_objects import ScheduleType
from modules.event.events import EventScheduleAdded
from modules.event.repository import EventRepository
from pointsheet.domain.types import EntityId
from pointsheet.domain.exceptions.base import PointSheetValidationError


class AddEventSchedule(Command):
    event_id: EntityId
    type: ScheduleType
    nbr_of_laps: Optional[NonNegativeInt] = None
    duration: Optional[str] = None

    @model_validator(mode="after")
    def validate_nbr_of_laps(self) -> Self:
        if (
            self.type in [ScheduleType.race, ScheduleType.qualification]
            and self.duration is None
        ):
            raise PointSheetValidationError(
                message=f"When the schedule is {ScheduleType.race} or {ScheduleType.qualification},duration must be set."
            )

        return self


@event_module.handler(AddEventSchedule)
def handle_add_event_schedule(
    cmd: AddEventSchedule, ctx: TransactionContext, repo: EventRepository
):
    event = repo.find_by_id(cmd.event_id)

    if not event:
        raise EventNotFoundException()

    schedule = Schedule(**cmd.model_dump(exclude={"event_id", "id"}))
    try:
        event.add_schedule(schedule)
        repo.update(event)
        ctx.publish(EventScheduleAdded(event_id=cmd.event_id))
    except ValueError as e:
        raise PointSheetValidationError(message=str(e))
