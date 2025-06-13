import datetime
from uuid import uuid4

import pytest

from modules.event.domain.value_objects import SeriesStatus, DriverResult
from pointsheet.domain.types import EntityId
from pointsheet.factories.account import UserFactory
from pointsheet.factories.event import SeriesFactory, EventFactory
from pointsheet.models import Event, Series
from pointsheet.models.event import RaceResult, EventSchedule, Participants


def test_we_can_create_a_series_without_status_set(db_session):
    series = Series(title="Home 1")
    db_session.add(series)
    db_session.commit()


def test_create_series_without_associated_event(db_session):
    series = Series(title="Home 2", status=SeriesStatus.started)
    db_session.add(series)
    db_session.commit()
    assert series.id is not None


def test_one_off_event_without_series_association(db_session):
    event = Event(title="Event 1", host=EntityId(int=1))
    db_session.add(event)
    db_session.commit()
    assert event.id is not None


def test_create_event_associated_with_series(db_session):
    series = SeriesFactory(title="New series", status=SeriesStatus.started, session=db_session)
    event = Event(id=uuid4(), title="event 1", host=uuid4())
    series.events.append(event)
    db_session.merge(series)
    db_session.commit()

    assert event.id is not None
    assert series.id is not None
    assert len(series.events) == 1


def test_series_fails_when_date_is_in_past(db_session):
    with pytest.raises(ValueError):
        past_date = datetime.datetime(2024, 1, 1)
        series = Series(title="Past series", starts_at=past_date)
        db_session.add(series)
        db_session.commit()


def test_series_ends_at_cannot_be_in_past_if_starts_at_is_set(db_session):
    with pytest.raises(ValueError):
        ends_at = datetime.datetime(2024, 1, 1)
        series = Series(
            title="Past series",
            starts_at=datetime.datetime.now(),
            ends_at=ends_at,
            status=SeriesStatus.started,
        )
        db_session.add(series)
        db_session.commit()


def test_add_multiple_race_schedules_to_event(db_session):
    event = EventFactory(session=db_session)

    driver1 = Participants(event_id=event.id, name="driver1", id=uuid4())
    driver2 = Participants(event_id=event.id, name="driver2", id=uuid4())

    db_session.add(driver1)
    db_session.add(driver2)

    schedule1 = EventSchedule(nbr_of_laps=20, duration="2 hours", type="race")
    schedule2 = EventSchedule(nbr_of_laps=15, duration="1.5 hours", type="race")

    driver_result1 = DriverResult(
        driver_id=driver1.id,
        driver=driver1.name,
        position=1,
        best_lap="00:32:00",
        total="01:38:00",
        points=25,
        total_points=25,
    )

    driver_result2 = DriverResult(
        driver_id=driver2.id,
        driver=driver2.name,
        position=2,
        best_lap="00:33:00",
        total="01:40:00",
        points=18,
        total_points=18,
    )

    race_result1 = RaceResult(
        result=[driver_result1, driver_result2], schedule=schedule1
    )
    race_result2 = RaceResult(
        result=[driver_result1, driver_result2], schedule=schedule2
    )

    schedule1.result = race_result1
    schedule2.result = race_result2

    event.schedule.extend([schedule1, schedule2])
    db_session.merge(event)
    db_session.commit()

    assert len(event.schedule) == 2


def test_save_race_result_to_event(patch_session):
    session = next(patch_session)

    event = EventFactory(session=session)
    schedule = EventSchedule(nbr_of_laps=10, duration="1 hour", type="race")

    driver = UserFactory(session=session)

    driver_result = DriverResult(
        driver_id=driver.id,
        driver=driver.name,
        position=1,
        best_lap="00:34:00",
        total="01:43:00",
        points=10,
        total_points=10,
    )

    race_result = RaceResult(result=[driver_result])
    schedule.result = race_result
    event.schedule.append(schedule)

    session.merge(event)
    session.commit()
