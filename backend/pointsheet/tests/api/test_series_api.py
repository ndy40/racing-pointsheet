from contextlib import nullcontext
from http import HTTPStatus

from fastjsonschema import validate

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
    with nullcontext():
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
