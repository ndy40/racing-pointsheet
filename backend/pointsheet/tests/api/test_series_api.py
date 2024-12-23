from http import HTTPStatus

from modules.event.domain.value_objects import SeriesStatus


def test_create_series(client):
    payload = {
        "title": "Series 1",
        "status": "started",
        "starts_at": "2025-01-01T01:00:00",
        "ends_at": "2026-01-01T01:00:00",
    }
    resp = client.post("/series", json=payload)
    assert resp.status_code == HTTPStatus.OK


def test_create_series_defaults_to_not_started_status(client):
    payload = {
        "title": "Series 1",
        "starts_at": "2025-01-01T01:00:00",
        "ends_at": "2026-01-01T01:00:00",
    }
    resp = client.post("/series", json=payload)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json["status"] == SeriesStatus.not_started


def test_fetch_series_by_id(client, db_session, series_factory):
    series = series_factory(status=None)
    db_session.commit()

    resp = client.get(f"/series/{series.id}")
    assert str(series.id) == resp.json["id"]
    assert resp.json["status"] == SeriesStatus.not_started
