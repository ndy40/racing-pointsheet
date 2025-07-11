from typing import Optional, List

from lato import Command

from modules.event import event_module
from modules.event.repository import EventRepository, CarRepository
from modules.auth.exceptions import EventNotFoundException
from modules.event.domain.value_objects import EventStatus
from modules.event.domain.entity import Car
from pointsheet.domain.types import EntityId
from datetime import datetime


class UpdateEventModel(Command):
    event_id: EntityId
    title: Optional[str] = None
    host: Optional[EntityId] = None
    status: Optional[EventStatus] = None
    track: Optional[int] = None
    series: Optional[EntityId] = None
    rules: Optional[str] = None
    max_participants: Optional[int] = None
    cars: Optional[List[int]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    game: Optional[int] = None


@event_module.handler(UpdateEventModel)
def handle_update_event(cmd: UpdateEventModel, repo: EventRepository, car_repo: CarRepository):
    event = repo.find_by_id(cmd.event_id)
    if not event:
        return EventNotFoundException()

    field_to_update = cmd.model_dump(exclude_unset=True, exclude=("event_id", "cars"))
    for field, value in field_to_update.items():
        setattr(event, field, value)

    # Handle cars separately
    if event.cars and not cmd.cars:
        # if car is set as null or []
        event.remove_all_cars()
    elif cmd.cars:
        # Clear existing cars
        event.cars = []
        # Fetch car objects and add them
        car_objects = car_repo.find_by_ids(cmd.cars)
        for car in car_objects:
            event.add_car(car)

    repo.update(event)
    return None