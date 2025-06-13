import uuid

from pointsheet.factories.account import UserFactory


def test_get_all_drivers(client, auth_token, db_session):
    # Create some test drivers
    user1 = UserFactory(session=db_session)
    user2 = UserFactory(session=db_session)
    db_session.commit()

    # Make the request to get all drivers
    response = client.get("/api/accounts/drivers", headers=auth_token)
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the test drivers
    drivers = response.json
    assert len(drivers) >= 2  # There might be other drivers in the database
    
    # Check that the test drivers are in the response
    driver_ids = [driver["id"] for driver in drivers]
    assert str(user1.id) in driver_ids
    assert str(user2.id) in driver_ids


def test_get_driver_by_id(client, auth_token, db_session):
    # Create a test driver
    user = UserFactory(session=db_session)
    db_session.commit()

    # Make the request to get the driver by ID
    response = client.get(f"/api/accounts/drivers/{user.id}", headers=auth_token)
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the correct driver
    driver = response.json
    assert driver["id"] == str(user.id)
    assert driver["name"] == user.name


def test_get_non_existent_driver_returns_404(client, auth_token):
    # Generate a random UUID for a non-existent driver
    non_existent_id = uuid.uuid4()

    # Make the request to get a non-existent driver
    response = client.get(f"/api/accounts/drivers/{non_existent_id}", headers=auth_token)
    
    # Check that the response is a 404
    assert response.status_code == 404