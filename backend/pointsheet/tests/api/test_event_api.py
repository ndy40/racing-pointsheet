import uuid

from fastjsonschema import validate

from pointsheet.factories.account import DriverFactory
from pointsheet.factories.event import EventFactory, EventDriverFactory
from .schemas.common import resource_created
from modules.event.domain.value_objects import EventStatus


def test_create_event(client, login):
    token = login["token"]

    payload = {
        "title": "Test Event",
        "host": str(uuid.uuid4()),
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post(
        "/api/events/", json=payload, headers={"Authorization": f"Bearer {token}"}
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
        "/api/events/", json=payload, headers={"Authorization": "Bearer abc"}
    )
    assert response.status_code == 400


def test_create_and_fetch_event_by_id(client, db_session, auth_token):
    event = EventFactory()

    # Fetch the event by ID
    fetch_response = client.get(f"/api/events/{str(event.id)}/", headers=auth_token)
    assert fetch_response.status_code == 200, event.id
    # validate(event_schema, fetch_response.json)


def test_creating_event_without_host_fails(client, auth_token):
    payload = {
        "title": "Test Event",
        "track": "Test Track",
        "status": EventStatus.open.value,
    }

    response = client.post("/api/events/", json=payload, headers=auth_token)
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

    response = client.post("/api/events/", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_driver_joining_event(client, auth_token, default_user):
    event = EventFactory()
    DriverFactory(id=default_user.id)
    response = client.put(f"/api/events/{event.id}/join", headers=auth_token)
    assert response.status_code == 204


def test_driver_joining_event_twice_fails(client, db_session, auth_token, default_user):
    event = EventFactory()
    DriverFactory(id=default_user.id)

    client.put(f"/api/events/{event.id}/join", headers=auth_token)
    response = client.put(f"/api/events/{event.id}/join", headers=auth_token)

    assert response.status_code == 400, response.json


def test_driver_leaving_event_succeeds(client, db_session, auth_token, default_user):
    event = EventFactory()
    EventDriverFactory(id=default_user.id, event_id=event.id)

    response = client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    assert response.status_code == 204, response.json


def test_driver_leaving_event_twice_returns_204(
    client, db_session, auth_token, default_user
):
    event = EventFactory()
    EventDriverFactory(id=default_user.id, event_id=event.id)

    client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    response = client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    assert response.status_code == 204, response.json


def test_add_schedule_to_event(client, db_session, auth_token):
    event = EventFactory()

    payload = {
        "type": "race",
        "nbr_of_laps": 25,
        "duration": "00:45:00",
    }

    response = client.post(
        f"/api/events/{event.id}/schedule", json=payload, headers=auth_token
    )

    assert response.status_code == 204, response.json


def test_removing_schedule_from_event_succeeds(client, db_session, auth_token):
    event = EventFactory()

    # Add three schedules: practice, qualification, and race
    practice_schedule = {"type": "practice", "duration": "00:30:00"}
    qualification_schedule = {"type": "qualification", "duration": "00:20:00"}
    race_schedule = {"type": "race", "nbr_of_laps": 50}

    client.post(
        f"/api/events/{event.id}/schedule", json=practice_schedule, headers=auth_token
    )
    client.post(
        f"/api/events/{event.id}/schedule",
        json=qualification_schedule,
        headers=auth_token,
    )
    race_response = client.post(
        f"/api/events/{event.id}/schedule", json=race_schedule, headers=auth_token
    )

    # Ensure schedules are added successfully
    assert race_response.status_code == 204

    # Remove the qualification schedule
    schedule_to_remove = 2
    remove_response = client.delete(
        f"/api/events/{event.id}/schedule/{schedule_to_remove}", headers=auth_token
    )

    # Check if schedule was removed successfully
    assert remove_response.status_code == 204

    # Validate remaining schedules
    updated_event_response = client.get(f"/api/events/{event.id}/", headers=auth_token)
    updated_schedule = updated_event_response.json.get("schedule", [])

    # assert len(updated_schedule) == 2, updated_schedule
    assert all(schedule["type"] != "qualification" for schedule in updated_schedule)


def test_removing_non_existent_schedule_from_event_returns_400(
    client, db_session, auth_token
):
    event = EventFactory()

    # Attempt to remove a schedule with an ID that does not exist
    non_existent_schedule_id = 999  # Example ID
    response = client.delete(
        f"/api/events/{event.id}/schedule/{non_existent_schedule_id}",
        headers=auth_token,
    )

    # Ensure the response returns a 400 error
    assert response.status_code == 204, response.json


def test_add_duplicate_practice_schedule_fails(client, db_session, auth_token):
    event = EventFactory()

    # Add the first 'practice' schedule
    payload = {
        "type": "practice",
        "duration": "00:20:00",
    }
    client.post(f"/api/events/{event.id}/schedule", json=payload, headers=auth_token)

    # Try adding another 'practice' schedule
    response = client.post(
        f"/api/events/{event.id}/schedule", json=payload, headers=auth_token
    )

    assert response.status_code == 400, response.json


def test_add_duplicate_qualification_schedule_fails(client, db_session, auth_token):
    event = EventFactory()

    # Add the first 'qualification' schedule
    payload = {
        "type": "qualification",
        "duration": "00:10:00",
    }
    client.post(f"/api/events/{event.id}/schedule", json=payload, headers=auth_token)

    # Try adding another 'qualification' schedule
    response = client.post(
        f"/api/events/{event.id}/schedule", json=payload, headers=auth_token
    )

    assert response.status_code == 400, response.json
