from http import HTTPStatus

from fastjsonschema import validate

from .schemas.auth import current_user_schema


def test_get_current_user_success(client, auth_token):
    """Test successful retrieval of current user information."""
    # Make request with valid auth token
    response = client.get("/api/auth", headers=auth_token)

    # Assert response status code and validate schema
    assert response.status_code == HTTPStatus.OK
    validate(current_user_schema, response.json)

    # Assert response contains expected data
    assert response.json["username"] == "testuser"
    assert response.json["role"] == "driver"
    assert "auth_expires_in" in response.json


def test_get_current_user_unauthorized(client):
    """Test unauthorized access to current user endpoint."""
    # Make request without auth token
    response = client.get("/api/auth")

    # Assert response status code
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    """Test access with invalid auth token."""
    # Make request with invalid auth token
    invalid_auth_header = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/auth", headers=invalid_auth_header)

    # Assert response status code
    assert response.status_code == HTTPStatus.UNAUTHORIZED
