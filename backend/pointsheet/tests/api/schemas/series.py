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

event_is_closed_after_update_under_series = {
    "type": "object",
    "required": ["id", "events"],
    "properties": {
        "id": {"type": "string"},
        "events": {
            "type": "array",
            "minItems": 1,
            "maxItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "status": {"type": "string", "const": "closed"},
                },
            },
        },
    },
}
