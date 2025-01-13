from contextlib import nullcontext
from http import HTTPStatus
from unittest.mock import patch

from fastjsonschema import validate

from modules.event.domain.entity import Series
from modules.event.domain.value_objects import EventStatus, SeriesStatus
from modules.event.repository import SeriesRepository
from .schemas.series import (
    create_series_no_events_schema,
    create_series_defaults_to_not_started_status_schema,
)


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_create_series(_, client, start_end_date_future):
    start_date, end_date = start_end_date_future

    payload = {
        "title": "Series 1",
        "status": "started",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    resp = client.post("/series", json=payload, headers={"Authorization": "Bearer abc"})
    validate(create_series_no_events_schema, resp.json)
    assert resp.status_code == HTTPStatus.OK


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_create_series_defaults_to_not_started_status(_, client, start_end_date_future):
    start_date, end_date = start_end_date_future
    payload = {
        "title": "Series 1",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    with nullcontext():
        resp = client.post(
            "/series", json=payload, headers={"Authorization": "Bearer abc"}
        )
        validate(create_series_defaults_to_not_started_status_schema, resp.json)
        assert resp.status_code == HTTPStatus.OK


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_fetch_series_by_id(_, client, db_session, series_factory):
    series = series_factory(status=None)
    db_session.commit()

    with nullcontext():
        resp = client.get(
            f"/series/{series.id}", headers={"Authorization": "Bearer abc"}
        )
        validate(create_series_no_events_schema, resp.json)
        assert str(series.id) == resp.json["id"]


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_add_event_to_series(_, client, series_factory, db_session):
    series = series_factory()
    db_session.commit()
    event_payload = {
        "title": "Main race",
        "status": EventStatus.open,
        "host": "0e90c9a1-7732-46dc-95f0-4d0aad25da1e",
    }

    resp = client.post(
        f"/series/{series.id}/events",
        json=event_payload,
        headers={"Authorization": "Bearer abc"},
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_update_event_in_series(_, client, series_factory, db_session, event_factory):
    event = event_factory(status=EventStatus.open)
    series = series_factory(status=SeriesStatus.started, events=[event])
    db_session.commit()

    payload = {"id": str(event.id), "status": EventStatus.closed}

    repo = SeriesRepository(db_session)
    resp = client.put(f"/series/{series.id}/events", json=payload)
    series: Series = repo.find_by_id(series.id)

    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json
    assert series.events[0].status == EventStatus.closed


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_delete_event_from_series(_, client, series_factory, db_session, event_factory):
    event = event_factory(status=EventStatus.open)
    series = series_factory(status=SeriesStatus.started, events=[event])
    db_session.commit()

    resp = client.delete(f"/series/{series.id}/events/{event.id}/")
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_series_startus_cannot_be_started_after_close(
    _, client, db_session, series_factory
):
    series = series_factory(status=SeriesStatus.closed)
    db_session.commit()

    resp = client.put(
        f"/series/{series.id}/status", json={"status": SeriesStatus.started.value}
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST
