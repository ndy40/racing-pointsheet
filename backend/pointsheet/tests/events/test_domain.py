from datetime import datetime, timedelta
import uuid

import pytest
from pydantic import ValidationError

from modules.event.domain.entity import Series, Event
from modules.event.domain.exceptions import InvalidEventDateForSeries
from modules.event.domain.value_objects import SeriesStatus


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
