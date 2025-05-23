# Schema definitions for authentication API tests

current_user_schema = {
    "type": "object",
    "required": ["username", "role"],
    "properties": {
        "username": {"type": "string"},
        "role": {"type": "string", "enum": ["driver", "admin"]},
        "auth_expires_in": {"type": ["string", "null"]},
    },
}

unauthorized_schema = {
    "type": "object",
    "required": ["error", "message"],
    "properties": {
        "error": {"type": "string"},
        "message": {"type": "string"},
    },
}
