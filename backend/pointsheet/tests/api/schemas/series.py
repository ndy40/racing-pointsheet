create_series_no_events_schema = {
    "type": "object",
    "required": ["id", "title", "status"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "status": {"type": "string"},
    },
}

create_series_defaults_to_not_started_status_schema = {
    "type": "object",
    "required": ["id", "status"],
    "properties": {
        "id": {"type": "string"},
        "status": {"type": "string", "const": "not_started"},
    },
}
