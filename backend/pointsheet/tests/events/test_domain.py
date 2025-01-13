from datetime import datetime, timedelta
import uuid

import pytest
from pydantic import ValidationError
from modules.event.domain.entity import Schedule

from modules.event.domain.entity import Series, Event
from modules.event.domain.exceptions import InvalidEventDateForSeries
from modules.event.domain.value_objects import SeriesStatus, ScheduleType


def test_add_event_to_series_fails_when_event_in_past():
    now_date = datetime.now() + timedelta(hours=1)
    end_date = now_date + timedelta(days=2)

    series = Series(
        title="Event 1",
        status=SeriesStatus.not_started,
        starts_at=now_date,
        ends_at=end_date,
    )

    event = Event(
        title="Spring 1",
        host=uuid.uuid4(),
        starts_at=now_date + timedelta(days=-1),
        ends_at=end_date,
    )

    with pytest.raises(InvalidEventDateForSeries):
        series.add_event(event)


def test_add_event_to_series_fails_when_event_ends_after_series_ends():
    now_date = datetime.now() + timedelta(hours=1)
    end_date = now_date + timedelta(days=2)

    series = Series(
        title="Event 1",
        status=SeriesStatus.not_started,
        starts_at=now_date,
        ends_at=end_date,
    )

    event = Event(
        title="Spring 1",
        host=uuid.uuid4(),
        starts_at=now_date + timedelta(days=1),
        ends_at=end_date + timedelta(days=1),
    )

    with pytest.raises(InvalidEventDateForSeries):
        series.add_event(event)


def test_event_creation_fails_when_start_but_no_end_date():
    now_date = datetime.now() + timedelta(hours=1)
    with pytest.raises(ValidationError):
        Event(
            title="Spring 1",
            host=uuid.uuid4(),
            starts_at=now_date + timedelta(days=1),
        )


def test_adding_driver_to_event_does_not_accept_duplicate():
    from modules.event.domain.entity import Driver  # Ensure Driver is imported

    event = Event(
        title="Summer 1",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )

    driver = Driver(driver_id=uuid.uuid4(), name="John Doe")  # Instantiate a Driver
    event.add_driver(driver)  # Adding a driver for the first time

    initial_driver_count = len(event.drivers)
    event.add_driver(driver)  # Attempting to add the same driver again
    assert len(event.drivers) == initial_driver_count  # Ensure length remains unchanged


def test_removing_driver_from_event():
    from modules.event.domain.entity import Driver  # Ensure Driver is imported

    event = Event(
        title="Summer 1",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )

    driver = Driver(driver_id=uuid.uuid4(), name="Jane Doe")  # Instantiate a Driver
    event.add_driver(driver)  # Add the driver
    assert driver in event.drivers  # Ensure the driver is added

    event.remove_driver(driver.driver_id)  # Remove the driver
    assert driver not in event.drivers  # Ensure the driver is removed


def test_adding_schedules_to_event_maintains_order():
    event = Event(
        title="Winter Grand Prix",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=3),
    )

    qualification = Schedule(id=uuid.uuid4().int, type=ScheduleType.qualification)
    practice = Schedule(id=uuid.uuid4().int, type=ScheduleType.practice)
    race = Schedule(id=uuid.uuid4().int, type=ScheduleType.race)

    event.add_schedule(qualification)
    event.add_schedule(race)
    event.add_schedule(practice)

    schedule_types = [schedule.type.value for schedule in event.schedule]
    assert schedule_types == ["practice", "qualification", "race"]
