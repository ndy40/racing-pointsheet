event_schema = {
    "type": "object",
    "required": ["id", "title", "host", "starts_at", "ends_at", "status"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "host": {"type": "string"},
        "starts_at": {"type": "string", "format": "date-time"},
        "ends_at": {"type": "string", "format": "date-time"},
        "track": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "closed", "in_progress"]},
    },
}
