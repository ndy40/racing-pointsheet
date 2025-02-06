import datetime
from uuid import uuid4

import pytest

from modules.event.domain.value_objects import SeriesStatus, DriverResult
from pointsheet.domain import EntityId
from pointsheet.factories.account import DriverFactory
from pointsheet.factories.event import SeriesFactory, EventFactory
from pointsheet.models import Event, Series
from pointsheet.models.event import RaceResult, EventSchedule


def test_we_can_create_a_series_without_status_set(db_session):
    series = Series(title="Series 1")
    db_session.add(series)
    db_session.commit()


def test_create_series_without_associated_event(db_session):
    series = Series(title="Series 2", status=SeriesStatus.started)
    db_session.add(series)
    db_session.commit()
    assert series.id is not None


def test_one_off_event_without_series_association(db_session):
    event = Event(title="Event 1", host=EntityId(int=1))
    db_session.add(event)
    db_session.commit()
    assert event.id is not None


def test_create_event_associated_with_series(db_session):
    series = SeriesFactory(title="New series", status=SeriesStatus.started)
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


def test_save_race_result_to_event(db_session):
    event = EventFactory()
    schedule = EventSchedule(nbr_of_laps=10, duration="1 hour", type="race")

    driver = DriverFactory()

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

    db_session.merge(event)
    db_session.commit()
