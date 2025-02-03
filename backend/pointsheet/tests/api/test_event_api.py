import logging
import uuid

from fastjsonschema import validate

from pointsheet.factories.account import DriverFactory
from pointsheet.factories.event import EventFactory
from .schemas.common import resource_created
from modules.event.domain.value_objects import EventStatus


logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


def test_create_event(client, login):
    token = login["token"]

    payload = {
        "title": "Test Event",
        "host": str(uuid.uuid4()),
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post(
        "/events/", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    validate(resource_created, response.json)
    assert response.status_code == 201


def test_create_event_with_ends_at_past_of_starts_at(client):
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


def test_create_and_fetch_event_by_id(client, db_session, auth_token):
    event = EventFactory()

    # Fetch the event by ID
    fetch_response = client.get(f"/events/{str(event.id)}/", headers=auth_token)
    assert fetch_response.status_code == 200, event.id
    # validate(event_schema, fetch_response.json)


def test_creating_event_without_host_fails(client, auth_token):
    payload = {
        "title": "Test Event",
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post("/events/", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_create_event_with_ends_at_exceeds_one_month_of_starts_at(client, auth_token):
    payload = {
        "title": "Long Duration Event",
        "host": str(uuid.uuid4()),
        "track": "Special Track",
        "status": EventStatus.open,
        "starts_at": "2023-11-10T15:00:00Z",
        "ends_at": "2023-12-15T15:00:00Z",  # 35 days later
    }

    response = client.post("/events/", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_driver_joining_event(client, db_session, auth_token, default_user):
    event = EventFactory()
    DriverFactory(id=default_user.id)

    response = client.put(f"/events/{event.id}/join", headers=auth_token)

    assert response.status_code == 204


def test_driver_joining_event_twice_fails(client, db_session, auth_token, default_user):
    event = EventFactory()
    DriverFactory(id=default_user.id)

    client.put(f"/events/{event.id}/join", headers=auth_token)
    response = client.put(f"/events/{event.id}/join", headers=auth_token)

    assert response.status_code == 400
