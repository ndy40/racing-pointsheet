from contextlib import nullcontext
from http import HTTPStatus

from fastjsonschema import validate

from modules.event.domain.entity import Series
from modules.event.domain.value_objects import EventStatus, SeriesStatus
from modules.event.repository import SeriesRepository
from .schemas.series import (
    create_series_no_events_schema,
    create_series_defaults_to_not_started_status_schema,
)


def test_create_series(client):
    payload = {
        "title": "Series 1",
        "status": "started",
        "starts_at": "2025-01-01T01:00:00",
        "ends_at": "2026-01-01T01:00:00",
    }
    # with nullcontext():
    resp = client.post("/series", json=payload)
    validate(create_series_no_events_schema, resp.json)
    assert resp.status_code == HTTPStatus.OK


def test_create_series_defaults_to_not_started_status(client):
    payload = {
        "title": "Series 1",
        "starts_at": "2025-01-01T01:00:00",
        "ends_at": "2026-01-01T01:00:00",
    }
    with nullcontext():
        resp = client.post("/series", json=payload)
        validate(create_series_defaults_to_not_started_status_schema, resp.json)
        assert resp.status_code == HTTPStatus.OK


def test_fetch_series_by_id(client, db_session, series_factory):
    series = series_factory(status=None)
    db_session.commit()

    with nullcontext():
        resp = client.get(f"/series/{series.id}")
        validate(create_series_no_events_schema, resp.json)
        assert str(series.id) == resp.json["id"]


def test_add_event_to_series(client, series_factory, db_session):
    series = series_factory()
    db_session.commit()
    event_payload = {
        "title": "Main race",
        "status": EventStatus.open,
        "host": "0e90c9a1-7732-46dc-95f0-4d0aad25da1e",
    }

    resp = client.post(f"/series/{series.id}/events", json=event_payload)
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


def test_update_event_in_series(client, series_factory, db_session, event_factory):
    event = event_factory(status=EventStatus.open)
    series = series_factory(status=SeriesStatus.started, events=[event])
    db_session.commit()

    payload = {"id": str(event.id), "status": EventStatus.closed}

    repo = SeriesRepository(db_session)
    resp = client.put(f"/series/{series.id}/events", json=payload)
    series: Series = repo.find_by_id(series.id)

    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json
    assert series.events[0].status == EventStatus.closed


def test_delete_event_from_series(client, series_factory, db_session, event_factory):
    event = event_factory(status=EventStatus.open)
    series = series_factory(status=SeriesStatus.started, events=[event])
    db_session.commit()

    resp = client.delete(f"/series/{series.id}/events/{event.id}/")
    assert resp.status_code == HTTPStatus.NO_CONTENT, (event.id, series.id)
