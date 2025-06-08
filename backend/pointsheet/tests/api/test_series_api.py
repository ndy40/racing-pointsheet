import uuid
import io
from contextlib import nullcontext
from http import HTTPStatus
from datetime import datetime, timedelta

import pytest
from fastjsonschema import validate
from werkzeug.datastructures import FileStorage

from modules import SeriesRepository
from modules.event.domain.value_objects import EventStatus, SeriesStatus
from pointsheet.factories.event import SeriesFactory, EventFactory
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
        "description": "This is a test series description",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    resp = client.post("/api/series", json=payload, headers=auth_token)
    validate(resource_created, resp.json)
    assert resp.status_code == HTTPStatus.CREATED


def test_create_series_defaults_to_not_started_status(
    client, start_end_date_future, auth_token
):
    start_date, end_date = start_end_date_future
    payload = {
        "title": "Home 1",
        "description": "This is a test series with default status",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    with nullcontext():
        resp = client.post("/api/series", json=payload, headers=auth_token)
        validate(resource_created, resp.json)
        assert resp.status_code == HTTPStatus.CREATED


def test_fetch_series_by_id(client, db_session, auth_token):
    series = SeriesFactory(status=None)

    with nullcontext():
        resp = client.get(f"/api/series/{series.id}", headers=auth_token)
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
        f"/api/series/{series.id}/events", json=event_payload, headers=auth_token
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


@pytest.mark.skip(reason="clean up required")
def test_update_event_in_series(client, db_session, auth_token):
    event = Event(title='Event 1', host=uuid.uuid4(), status=EventStatus.open,)
    series = SeriesFactory(status=SeriesStatus.started, events=[event])
    db_session.commit()

    series_repo = SeriesRepository(db_session)
    series = series_repo.find_by_id(series.id)
    event = series.events[0]

    assert event.status == EventStatus.open, event.status

    payload = {"id": str(event.id), "status": EventStatus.closed}
    update_resp = client.put(f"/api/series/{series.id}/events", json=payload, headers=auth_token)
    assert update_resp.status_code == HTTPStatus.NO_CONTENT, update_resp.json

    resp = client.get(f"/api/series/{series.id}", json=payload, headers=auth_token)
    assert resp.status_code != HTTPStatus.OK, resp.json
    validate(event_is_closed_after_update_under_series, resp.json)
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


def test_delete_event_from_series(client, db_session, auth_token):
    id = uuid.uuid4()
    event = Event(id=id, status=EventStatus.open, host=uuid.uuid4(), title="Event 1")
    series = SeriesFactory(status=SeriesStatus.started, events=[event])

    resp = client.delete(f"/api/series/{series.id}/events/{id}/", headers=auth_token)
    assert resp.status_code == HTTPStatus.NO_CONTENT, resp.json


def test_fetch_events_for_series(client, db_session, auth_token):
    # Create events with known IDs
    event1_id = uuid.uuid4()
    event2_id = uuid.uuid4()

    # Create events
    event1 = Event(id=event1_id, status=EventStatus.open, host=uuid.uuid4(), title="Event 1")
    event2 = Event(id=event2_id, status=EventStatus.open, host=uuid.uuid4(), title="Event 2")

    # Create a series with the events
    series = SeriesFactory(status=SeriesStatus.started, events=[event1, event2])
    db_session.commit()

    # Call the endpoint
    resp = client.get(f"/api/series/{series.id}/events", headers=auth_token)

    # Verify the response
    assert resp.status_code == HTTPStatus.OK
    assert len(resp.json) == 2

    # Verify the events are in the response
    event_ids = [event["id"] for event in resp.json]
    assert str(event1_id) in event_ids
    assert str(event2_id) in event_ids


def test_series_startus_cannot_be_started_after_close(client, db_session, auth_token):
    series = SeriesFactory(status=SeriesStatus.closed)
    db_session.commit()

    resp = client.put(
        f"/api/series/{series.id}/status",
        json={"status": SeriesStatus.started.value},
        headers=auth_token,
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_series_creation_with_cover_image_upload(
    client, start_end_date_future, auth_token, db_session
):
    """Test creating a series and then uploading a cover image for it."""
    # Step 1: Create a series
    start_date, end_date = start_end_date_future
    payload = {
        "title": "Series with Cover Image",
        "status": "started",
        "description": "This is a series with a cover image",
        "starts_at": start_date.isoformat(),
        "ends_at": end_date.isoformat(),
    }
    create_resp = client.post("/api/series", json=payload, headers=auth_token)
    assert create_resp.status_code == HTTPStatus.CREATED
    series_id = create_resp.json["resource"]

    # Step 2: Upload a cover image for the series
    # Create a test image file
    test_image_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82"
    test_image = io.BytesIO(test_image_data)
    file = FileStorage(
        stream=test_image,
        filename="test_image.png",
        content_type="image/png",
    )

    # Upload the image
    upload_resp = client.post(
        f"/api/series/{series_id}/cover-image",
        data={"image": file},
        headers=auth_token,
        content_type="multipart/form-data",
    )
    assert upload_resp.status_code == HTTPStatus.NO_CONTENT

    # Step 3: Verify the cover image is correctly associated with the series
    fetch_resp = client.get(f"/api/series/{series_id}", headers=auth_token)
    assert fetch_resp.status_code == HTTPStatus.OK
    assert fetch_resp.json["cover_image"] is not None


def test_patch_series(client, db_session, auth_token):
    """Test updating a series using the PATCH endpoint."""
    # Create a series using the factory
    series = SeriesFactory(
        title="Original Title",
        description="Original Description",
        status=SeriesStatus.not_started,
    )
    db_session.commit()

    # New data for updating the series
    new_title = "Updated Title"
    new_description = "Updated Description"
    new_start_date = datetime.now() + timedelta(days=10)
    new_end_date = datetime.now() + timedelta(days=20)

    # Prepare the payload for the PATCH request
    update_payload = {
        "title": new_title,
        "description": new_description,
        "starts_at": new_start_date.isoformat(),
        "ends_at": new_end_date.isoformat(),
    }

    # Send the PATCH request
    patch_resp = client.patch(
        f"/api/series/{series.id}", json=update_payload, headers=auth_token
    )

    # Verify the response
    assert patch_resp.status_code == HTTPStatus.OK
    validate(resource_created, patch_resp.json)
    assert patch_resp.json["resource"] == str(series.id)

    # Fetch the updated series to verify changes
    fetch_resp = client.get(f"/api/series/{series.id}", headers=auth_token)
    assert fetch_resp.status_code == HTTPStatus.OK

    # Verify the series was updated correctly
    updated_series = fetch_resp.json
    assert updated_series["title"] == new_title, fetch_resp.json
    assert updated_series["description"] == new_description
