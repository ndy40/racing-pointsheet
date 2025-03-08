import uuid
from contextlib import nullcontext
from http import HTTPStatus

from fastjsonschema import validate

from modules.event.domain.value_objects import EventStatus, SeriesStatus
from pointsheet.factories.event import SeriesFactory
from pointsheet.models import Event
from .schemas.common import resource_created
from .schemas.series import (
    create_series_no_events_schema,
    event_is_closed_after_update_under_series,
)


def test_create_series(client, start_end_date_future, auth_token):
    start_date, end_date = start_end_date_future

    payload = {
        "title": "Home 1",
        "status": "started",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    resp = client.post("/series", json=payload, headers=auth_token)
    validate(resource_created, resp.json)
    assert resp.status_code == HTTPStatus.CREATED


def test_create_series_defaults_to_not_started_status(
    client, start_end_date_future, auth_token
):
    start_date, end_date = start_end_date_future
    payload = {
        "title": "Home 1",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    with nullcontext():
        resp = client.post("/series", json=payload, headers=auth_token)
        validate(resource_created, resp.json)
        assert resp.status_code == HTTPStatus.CREATED


def test_fetch_series_by_id(client, db_session, auth_token):
    series = SeriesFactory(status=None)

    with nullcontext():
        resp = client.get(f"/series/{series.id}", headers=auth_token)
        validate(create_series_no_events_schema, resp.json)
        assert str(series.id) == resp.json["id"]


def test_add_event_to_series(client, db_session, auth_token):
    series = SeriesFactory()
    db_session.commit()
    event_payload = {
        "title": "Main race",
        "status": EventStatus.open,
        "host": "0e90c9a1-7732-46dc-95f0-4d0aad25da1e",
    }

    resp = client.post(
        f"/series/{series.id}/events", json=event_payload, headers=auth_token
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


def test_update_event_in_series(client, db_session, auth_token):
    series = SeriesFactory(status=SeriesStatus.started)
    series.events.append(
        Event(
            id=uuid.uuid4(), title="Event 1", host=uuid.uuid4(), status=EventStatus.open
        )
    )
    db_session.merge(series)
    db_session.commit()

    event = series.events[0]

    payload = {"id": str(event.id), "status": EventStatus.closed}
    client.put(f"/series/{series.id}/events", json=payload, headers=auth_token)
    resp = client.get(f"/series/{series.id}", json=payload, headers=auth_token)

    validate(event_is_closed_after_update_under_series, resp.json)
    assert resp.status_code == HTTPStatus.OK, resp.json


def test_delete_event_from_series(client, db_session, auth_token):
    id = uuid.uuid4()
    event = Event(id=id, status=EventStatus.open, host=uuid.uuid4(), title="Event 1")
    series = SeriesFactory(status=SeriesStatus.started, events=[event])

    resp = client.delete(f"/series/{series.id}/events/{id}/", headers=auth_token)
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


def test_series_startus_cannot_be_started_after_close(client, db_session, auth_token):
    series = SeriesFactory(status=SeriesStatus.closed)
    db_session.commit()

    resp = client.put(
        f"/series/{series.id}/status",
        json={"status": SeriesStatus.started.value},
        headers=auth_token,
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST
