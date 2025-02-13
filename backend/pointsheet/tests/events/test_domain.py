from datetime import datetime, timedelta
import uuid

import pytest
from pydantic import ValidationError
from modules.event.domain.entity import Schedule, RaceResult

from modules.event.domain.entity import Series, Event, Driver
from modules.event.exceptions import (
    InvalidEventDateForSeries,
    DriverAlreadySingedUp,
)
from modules.event.domain.value_objects import SeriesStatus, ScheduleType, DriverResult


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


def test_add_event_to_series_fails_when_event_starts_and_ends_before_series():
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
        starts_at=now_date - timedelta(days=2),
        ends_at=now_date - timedelta(days=1),
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
    event = Event(
        title="Summer 1",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )

    driver = Driver(id=uuid.uuid4(), name="John Doe")  # Instantiate a Driver

    with pytest.raises(DriverAlreadySingedUp):
        event.add_driver(driver)  # Adding a driver for the first time
        event.add_driver(driver)  # Attempting to add the same driver again


def test_adding_driver_to_event_raises_error_for_duplicate():
    event = Event(
        title="Autumn Endurance 1",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=3),
        ends_at=datetime.now() + timedelta(days=4),
    )

    with pytest.raises(DriverAlreadySingedUp):  # Verify exception is raised
        driver = Driver(id=uuid.uuid4(), name="Jane Roe")  # Instantiate a Driver
        event.add_driver(driver)  # Adding a driver for the first time
        event.add_driver(driver)  # Try to add the driver again


def test_signing_driver_to_event_successful():
    event = Event(
        title="Fall Race",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=3),
        ends_at=datetime.now() + timedelta(days=5),
    )

    driver = Driver(id=uuid.uuid4(), name="Alex Doe")  # Instantiate a Driver
    event.add_driver(driver)  # Signing a driver up for the event

    assert driver in event.drivers  # Check if the driver was successfully added
    assert len(event.drivers) == 1  # Ensure the event now contains the driver


def test_removing_driver_from_event():
    event = Event(
        title="Summer 1",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )

    driver = Driver(id=uuid.uuid4(), name="Jane Doe")  # Instantiate a Driver
    event.add_driver(driver)  # Add the driver
    assert driver in event.drivers  # Ensure the driver is added

    event.remove_driver(driver.id)  # Remove the driver
    assert driver not in event.drivers  # Ensure the driver is removed


def test_add_event_to_series_fails_when_event_starts_and_ends_after_series():
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
        starts_at=end_date + timedelta(days=1),  # Event starts after the series ends
        ends_at=end_date + timedelta(days=2),  # Event also ends after the series ends
    )

    with pytest.raises(InvalidEventDateForSeries):
        series.add_event(event)


def test_event_ends_at_same_time_as_series_valid():
    now_date = datetime.now()
    series_end = now_date + timedelta(days=3)

    series = Series(
        title="Test Series",
        status=SeriesStatus.not_started,
        starts_at=now_date,
        ends_at=series_end,
    )

    event = Event(
        title="Event at series end",
        host=uuid.uuid4(),
        starts_at=now_date + timedelta(days=1),
        ends_at=series_end,
    )

    try:
        series.add_event(event)
    except InvalidEventDateForSeries:
        pytest.fail("Event ending at the exact time the series ends should be valid.")


def test_removing_nonexistent_driver_from_event():
    event = Event(
        title="Nonexistent Driver Test",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )

    driver = Driver(id=uuid.uuid4(), name="John Doe")  # Instantiate a Driver
    event.add_driver(driver)  # Add the driver
    assert driver in event.drivers  # Ensure the driver is added

    non_existent_driver_id = (
        uuid.uuid4()
    )  # Generate an ID not associated with any driver in the event
    event.remove_driver(
        non_existent_driver_id
    )  # Attempt to remove a driver with this ID

    # Ensure the original driver is still present and no other unexpected behavior occurs
    assert (
        driver in event.drivers
    )  # Verify that the original driver is still in the event
    assert (
        len(event.drivers) == 1
    )  # Confirm that the number of drivers remains unchanged


def test_adding_race_result_to_event_with_no_schedule_id_fails():
    event = Event(
        title="Championship Event Without Schedule",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=4),
    )

    # Create a RaceResult object with no valid schedule ID
    driver_result = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver A",
        position=1,
        best_lap="1:21.000",
        total="13:45.678",
        points=25,
    )
    race_result = RaceResult(
        schedule_id=100,  # An ID not associated with any schedule
        result=[driver_result],
        mark_down="Invalid schedule ID test case",
    )

    with pytest.raises(ValueError, match="Cannot add result as no schedules exist"):
        event.add_result(race_result)


def test_adding_result_with_mismatched_schedule_id_raises_error():
    event = Event(
        title="Mismatched Schedule Test Event",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=2),
        ends_at=datetime.now() + timedelta(days=4),
    )

    # Add a race schedule to the event with a specific ID
    race_schedule = Schedule(id=10, type=ScheduleType.race, nbr_of_laps=10)
    event.add_schedule(race_schedule)

    # Create a RaceResult with a mismatched schedule_id
    driver_result = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver A",
        position=1,
        best_lap="1:24.456",
        total="15:30.567",
        points=25,
    )
    mismatched_result = RaceResult(
        schedule_id=99,  # This ID does not exist in event schedules
        result=[driver_result],
        mark_down="Invalid schedule ID test",
    )

    with pytest.raises(
        ValueError, match="Schedule ID 99 is not associated with a 'race' schedule."
    ):
        event.add_result(mismatched_result)


def test_adding_schedules_to_event_maintains_order():
    event = Event(
        title="Winter Grand Prix",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=3),
    )

    qualification = Schedule(type=ScheduleType.qualification)
    practice = Schedule(type=ScheduleType.practice)
    race = Schedule(type=ScheduleType.race)

    event.add_schedule(qualification)
    event.add_schedule(race)
    event.add_schedule(practice)

    schedule_types = [schedule.type.value for schedule in event.schedule]
    assert schedule_types == ["practice", "qualification", "race"]


def test_adding_two_race_schedules_maintains_order():
    event = Event(
        title="Winter Grand Prix",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=3),
    )
    race1 = Schedule(type=ScheduleType.qualification, nbr_of_laps=3)
    race2 = Schedule(type=ScheduleType.race, nbr_of_laps=5)
    race3 = Schedule(type=ScheduleType.race, nbr_of_laps=10)

    event.add_schedule(race1)
    event.add_schedule(race2)
    event.add_schedule(race3)

    assert event.schedule == [race1, race2, race3]


def test_adding_multiple_race_results_sorted_by_schedule_id():
    event = Event(
        title="Championship Event",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=4),
    )

    # Create race schedules with unique IDs
    race1 = Schedule(id=1, type=ScheduleType.race, nbr_of_laps=5)
    race2 = Schedule(id=2, type=ScheduleType.race, nbr_of_laps=10)

    event.add_schedule(race1)
    event.add_schedule(race2)

    # Add driver results to RaceResult objects
    driver1 = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver A",
        position=1,
        best_lap="1:20.000",
        total="15:00.000",
        points=25,
    )
    driver2 = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver B",
        position=2,
        best_lap="1:22.000",
        total="15:20.000",
        points=18,
    )

    result1 = RaceResult(
        schedule_id=2,
        result=[driver1, driver2],
        mark_down="Race 2 results",
    )
    result2 = RaceResult(
        schedule_id=1,
        result=[driver2, driver1],
        mark_down="Race 1 results",
    )

    # Add results to the event
    event.add_result(result1)
    event.add_result(result2)

    # Assert that the RaceResults are sorted by scheduleId
    assert len(event.results) == 2
    assert event.results[0].schedule_id == 1
    assert event.results[1].schedule_id == 2


def test_adding_race_result_to_event():
    event = Event(
        title="Championship Race",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=2),
        ends_at=datetime.now() + timedelta(days=4),
    )
    race_schedule = Schedule(id=1, type=ScheduleType.race, nbr_of_laps=10)
    event.add_schedule(race_schedule)

    driver_result = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver A",
        position=1,
        best_lap="1:23.456",
        total="15:34.567",
        points=25,
    )
    race_result = RaceResult(
        schedule_id=race_schedule.id, result=[driver_result], mark_down="Great race!"
    )

    event.add_result(race_result)

    assert len(event.results) == 1
    assert event.results[0].schedule_id == race_schedule.id
    assert event.results[0].result[0].driver == "Driver A"
    assert event.results[0].mark_down == "Great race!"


def test_adding_qualification_result_does_not_update_event_results():
    event = Event(
        title="Qualification Test Event",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=3),
    )

    qualification_schedule = Schedule(
        id=1, type=ScheduleType.qualification, nbr_of_laps=None
    )
    event.add_schedule(qualification_schedule)

    driver_result = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver B",
        position=1,
        best_lap="1:15.123",
        total="10:30.456",
        points=0,
    )
    qualification_result = RaceResult(
        schedule_id=qualification_schedule.id,
        result=[driver_result],
        mark_down="Not a race result",
    )

    with pytest.raises(
        ValueError, match="Schedule ID 1 is not associated with a 'race' schedule."
    ):
        event.add_result(qualification_result)

    assert len(event.results) == 0


def test_creating_event_with_invalid_dates_fails():
    with pytest.raises(ValidationError):
        Event(
            title="Winter Grand Prix",
            host=uuid.uuid4(),
            starts_at=datetime.now(),
            ends_at=datetime.now() + timedelta(days=-2),
        )


def test_removing_race_result_from_event():
    event = Event(
        title="Grand Finale",
        host=uuid.uuid4(),
        starts_at=datetime.now() + timedelta(days=2),
        ends_at=datetime.now() + timedelta(days=5),
    )

    # Create race schedules
    race1 = Schedule(id=1, type=ScheduleType.race, nbr_of_laps=10)
    race2 = Schedule(id=2, type=ScheduleType.race, nbr_of_laps=20)
    race3 = Schedule(id=3, type=ScheduleType.race, nbr_of_laps=15)

    # Add schedules to the event
    event.add_schedule(race1)
    event.add_schedule(race2)
    event.add_schedule(race3)

    # Create driver results for each schedule
    driver_result1 = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver A",
        position=1,
        best_lap="1:30.000",
        total="18:00.000",
        points=25,
    )
    race_result1 = RaceResult(
        schedule_id=1, result=[driver_result1], mark_down="Race 1 results"
    )

    driver_result2 = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver B",
        position=2,
        best_lap="1:32.000",
        total="19:00.000",
        points=18,
    )
    race_result2 = RaceResult(
        schedule_id=2, result=[driver_result2], mark_down="Race 2 results"
    )

    driver_result3 = DriverResult(
        driver_id=uuid.uuid4(),
        driver="Driver C",
        position=3,
        best_lap="1:33.000",
        total="19:30.000",
        points=15,
    )
    race_result3 = RaceResult(
        schedule_id=3, result=[driver_result3], mark_down="Race 3 results"
    )

    # Add race results to the event
    event.add_result(race_result1)
    event.add_result(race_result2)
    event.add_result(race_result3)

    # Ensure all results are added
    assert len(event.results) == 3

    # Remove the second race result
    event.remove_result(schedule_id=2)

    # Check that the race result has been removed
    assert len(event.results) == 2
    assert all(result.schedule_id != 2 for result in event.results)
    assert event.results[0].schedule_id == 1
    assert event.results[1].schedule_id == 3
