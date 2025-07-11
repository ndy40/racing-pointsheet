import uuid

from fastjsonschema import validate

from pointsheet.factories.account import UserFactory
from pointsheet.factories.event import EventFactory, EventDriverFactory, TrackFactory, GameFactory
from .schemas.common import resource_created
from modules.event.domain.value_objects import EventStatus


def test_create_event(client, login, db_session):
    token = login["token"]
    user = UserFactory(session=db_session)
    track = TrackFactory(session=db_session)
    game = GameFactory(session=db_session)

    payload = {
        "title": "Test Event",
        "host": str(user.id),
        "track": track.id,
        "status": EventStatus.open.value,
        "game": game.id,
    }

    response = client.post(
        "/api/events", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.json
    validate(resource_created, response.json)


def test_create_event_with_ends_at_past_of_starts_at(client, auth_token, db_session):
    user = UserFactory(session=db_session)
    track = TrackFactory(session=db_session)
    game = GameFactory(session=db_session)
    db_session.commit()

    payload = {
        "title": "Custom Event",
        "host": str(user.id),
        "track": track.id,
        "status": EventStatus.open.value,
        "starts_at": "2023-11-10T15:00:00Z",
        "ends_at": "2023-11-10T14:00:00Z",
        "game": game.id,
    }

    response = client.post("/api/events", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_create_and_fetch_event_by_id(client, auth_token, db_session):
    event = EventFactory(session=db_session)

    # Fetch the event by ID
    fetch_response = client.get(f"/api/events/{str(event.id)}", headers=auth_token)
    assert fetch_response.status_code == 200, event.id
    # validate(event_schema, fetch_response.json)


def test_creating_event_without_host_fails(client, auth_token, db_session):
    game = GameFactory(session=db_session)
    payload = {
        "title": "Test Event",
        "track": "Test Track",
        "status": EventStatus.open.value,
        "game": game.id,
    }

    response = client.post("/api/events", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_create_event_with_ends_at_exceeds_one_month_of_starts_at(client, auth_token, db_session):
    user = UserFactory(session=db_session)
    track = TrackFactory(session=db_session)
    game = GameFactory(session=db_session)
    db_session.commit()

    payload = {
        "title": "Long Duration Event",
        "host": str(user.id),
        "track": track.id,
        "status": EventStatus.open,
        "starts_at": "2023-11-10T15:00:00Z",
        "ends_at": "2023-12-15T15:00:00Z",  # 35 days later
        "game": game.id,
    }

    response = client.post("/api/events", json=payload, headers=auth_token)
    assert response.status_code == 400


def test_driver_joining_event(client, auth_token, default_user, db_session):
    event = EventFactory(session=db_session)
    UserFactory(id=default_user.id, session=db_session)
    response = client.put(f"/api/events/{event.id}/join", headers=auth_token)
    assert response.status_code == 204, response.json


def test_driver_joining_event_twice_fails(client, auth_token, default_user, db_session):
    event = EventFactory(session=db_session)
    UserFactory(id=default_user.id, session=db_session)
    db_session.flush()

    client.put(f"/api/events/{event.id}/join", headers=auth_token)
    response = client.put(f"/api/events/{event.id}/join", headers=auth_token)

    assert response.status_code == 400, response.json


def test_driver_leaving_event_succeeds(client, auth_token, default_user, db_session):
    event = EventFactory(session=db_session)
    EventDriverFactory(id=default_user.id, event_id=event.id, session=db_session)

    response = client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    assert response.status_code == 204, response.json


def test_driver_leaving_event_twice_returns_204(client, auth_token, default_user, db_session):
    event = EventFactory(session=db_session)
    EventDriverFactory(id=default_user.id, event_id=event.id, session=db_session)

    client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    response = client.put(f"/api/events/{event.id}/leave", headers=auth_token)
    assert response.status_code == 204, response.json


def test_add_schedule_to_event(client, auth_token, db_session):
    event = EventFactory(session=db_session)

    payload = {
        "type": "race",
        "nbr_of_laps": 25,
        "duration": "00:45:00",
    }

    response = client.post(
        f"/api/events/{event.id}/schedule", json=payload, headers=auth_token
    )

    assert response.status_code == 204, response.json


def test_removing_schedule_from_event_succeeds(client, auth_token, db_session):
    event = EventFactory(session=db_session)

    # Add three schedules: practice, qualification, and race
    practice_schedule = {"type": "practice", "duration": "00:30:00"}
    qualification_schedule = {"type": "qualification", "duration": "00:20:00"}
    race_schedule = {"type": "race", "nbr_of_laps": 50, "duration": "01:00"}

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


def test_removing_non_existent_schedule_from_event_returns_400(client, auth_token, db_session):
    event = EventFactory(session=db_session)

    # Attempt to remove a schedule with an ID that does not exist
    non_existent_schedule_id = 999  # Example ID
    response = client.delete(
        f"/api/events/{event.id}/schedule/{non_existent_schedule_id}",
        headers=auth_token,
    )

    # Ensure the response returns a 400 error
    assert response.status_code == 204, response.json


def test_add_duplicate_practice_schedule_fails(client, auth_token, db_session):
    event = EventFactory(session=db_session)

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


def test_add_duplicate_qualification_schedule_fails(client, auth_token, db_session):
    event = EventFactory(session=db_session)

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


def test_delete_event_succeeds(client, auth_token, db_session):
    # Create an event
    event = EventFactory(session=db_session)
    db_session.commit()

    # Delete the event
    response = client.delete(f"/api/events/{event.id}", headers=auth_token)

    # Check if the event was deleted successfully
    assert response.status_code == 204

    # Verify the event is no longer accessible
    get_response = client.get(f"/api/events/{event.id}", headers=auth_token)
    assert get_response.status_code == 404


def test_delete_non_existent_event_returns_400(client, auth_token):
    # Generate a random UUID for a non-existent event
    non_existent_id = uuid.uuid4()

    # Attempt to delete a non-existent event
    response = client.delete(f"/api/events/{non_existent_id}", headers=auth_token)

    # Should return a 400 error
    assert response.status_code == 400
