import pytest
from sqlalchemy.exc import StatementError

from event.domain.value_objects import SeriesStatus
from pointsheet.models import Series


def test_we_cannot_create_a_series_without_status_set(db_session):
    with pytest.raises(StatementError):
        series = Series(title="Series 1")
        db_session.add(series)
        db_session.commit()


def test_create_series_without_associated_event(db_session):
    series = Series(title="Series 2", status=SeriesStatus.started)
    db_session.add(series)
    db_session.commit()
