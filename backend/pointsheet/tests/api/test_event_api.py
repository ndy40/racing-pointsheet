import logging
import uuid
from unittest.mock import patch

from fastjsonschema import validate

from .schemas.common import resource_created
from modules.event.domain.value_objects import EventStatus


logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_create_event(_, client):
    payload = {
        "title": "Test Event",
        "host": str(uuid.uuid4()),
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post(
        "/events/", json=payload, headers={"Authorization": "Bearer abc"}
    )
    validate(resource_created, response.json)
    assert response.status_code == 201


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_create_event_with_ends_at_past_of_starts_at(_, client):
    payload = {
        "title": "Custom Event",
        "host": str(uuid.uuid4()),
        "track": "Custom Track",
        "status": EventStatus.open.value,
        "starts_at": "2023-11-10T15:00:00Z",
        "ends_at": "2023-11-10T14:00:00Z",
    }

    response = client.post(
        "/events/", json=payload, headers={"Authorization": "Bearer abc"}
    )
    assert response.status_code == 400


@patch("api.utils.TimedSerializer.deserializer", return_value=("abc", 0))
def test_create_and_fetch_event_by_id(_, client, event_factory, db_session):
    event = event_factory()
    db_session.commit()

    # Fetch the event by ID
    fetch_response = client.get(
        f"/events/{str(event.id)}/", headers={"Authorization": "Bearer abc"}
    )
    assert fetch_response.status_code == 200, event.id
    # validate(event_schema, fetch_response.json)


def test_creating_event_without_host_fails(client):
    payload = {
        "title": "Test Event",
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post(
        "/events/", json=payload, headers={"Authorization": "Bearer abc"}
    )
    assert response.status_code == 400


def test_create_event_with_ends_at_exceeds_one_month_of_starts_at(client):
    payload = {
        "title": "Long Duration Event",
        "host": str(uuid.uuid4()),
        "track": "Special Track",
        "status": EventStatus.open,
        "starts_at": "2023-11-10T15:00:00Z",
        "ends_at": "2023-12-15T15:00:00Z",  # 35 days later
    }

    response = client.post(
        "/events/", json=payload, headers={"Authorization": "Bearer abc"}
    )
    assert response.status_code == 400
