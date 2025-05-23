from typing import List

from lato import Command

from modules.event import event_module
from modules.event.domain.value_objects import ScheduleId, Result
from modules.event.repository import EventRepository
from modules.event.use_case.save_race_result import SaveRaceResult
from pointsheet.domain.types import EntityId


class AddEventResult(Command):
    event_id: EntityId
    schedule_id: ScheduleId
    result: List[Result]


@event_module.handler(AddEventResult)
def handle_add_event_result(cmd: AddEventResult, repo: EventRepository):
    use_case = SaveRaceResult(repo)
    use_case(cmd.event_id, cmd.schedule_id, cmd.result)
