import uuid

from modules.event.domain.entity import Event, Schedule
from modules.event.domain.value_objects import EventStatus, ScheduleType
from modules.event.repository import EventRepository


def test_saving_schedule_to_event(db_session):
    event = Event(
        id=uuid.uuid4(),
        title="Event 1",
        status=EventStatus.open,
        host=uuid.uuid4(),
    )

    schedule = Schedule(type=ScheduleType.practice, nbr_of_laps=5)
    event.add_schedule(schedule)

    event_repo = EventRepository(db_session)
    event_repo.add(event)
    new_obj = event_repo.find_by_id(event.id)

    assert len(new_obj.schedule) > 0
    assert new_obj.schedule[0].id is not None


def test_saving_event_with_three_schedules(db_session):
    event = Event(
        id=uuid.uuid4(),
        title="Event 2",
        status=EventStatus.open,
        host=uuid.uuid4(),
    )

    practice_schedule = Schedule(type=ScheduleType.practice, nbr_of_laps=5)
    qualification_schedule = Schedule(type=ScheduleType.qualification, nbr_of_laps=10)
    race_schedule = Schedule(type=ScheduleType.race, nbr_of_laps=50)

    event.add_schedule(practice_schedule)
    event.add_schedule(qualification_schedule)
    event.add_schedule(race_schedule)

    event_repo = EventRepository(db_session)
    event_repo.add(event)
    new_obj = event_repo.find_by_id(event.id)

    assert len(new_obj.schedule) == 3
    assert new_obj.schedule[0].type == ScheduleType.practice
    assert new_obj.schedule[1].type == ScheduleType.qualification
    assert new_obj.schedule[2].type == ScheduleType.race


def test_removing_most_recent_schedule_with_four_schedules(db_session):
    event = Event(
        id=uuid.uuid4(),
        title="Event 4",
        status=EventStatus.open,
        host=uuid.uuid4(),
    )

    practice_schedule = Schedule(type=ScheduleType.practice, nbr_of_laps=5)
    qualification_schedule = Schedule(type=ScheduleType.qualification, nbr_of_laps=10)
    race_schedule_1 = Schedule(type=ScheduleType.race, nbr_of_laps=50)
    race_schedule_2 = Schedule(type=ScheduleType.race, nbr_of_laps=75)

    event.add_schedule(practice_schedule)
    event.add_schedule(qualification_schedule)
    event.add_schedule(race_schedule_1)
    event.add_schedule(race_schedule_2)

    event.remove_schedule(race_schedule_2)

    event_repo = EventRepository(db_session)
    event_repo.add(event)
    new_obj = event_repo.find_by_id(event.id)

    assert len(new_obj.schedule) == 4
    assert new_obj.schedule[0].type == ScheduleType.practice
    assert new_obj.schedule[1].type == ScheduleType.qualification
    assert new_obj.schedule[2].type == ScheduleType.race
    assert new_obj.schedule[2].nbr_of_laps == 50
