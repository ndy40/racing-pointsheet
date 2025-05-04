# Racing Pointsheet API Documentation

This document provides detailed information about the Racing Pointsheet API endpoints, request/response formats, and examples.

## Authentication

Most API endpoints require authentication. To authenticate, you need to obtain a token by logging in.

### Login

```
POST /api/auth/login
```

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "token": "your_auth_token",
  "user_id": "user_uuid"
}
```

**Usage:**
Include the token in the Authorization header for subsequent requests:

```
Authorization: Bearer your_auth_token
```

## Events

### Get All Events

```
GET /api/events/
```

**Response:**

```json
[
  {
    "id": "event_uuid",
    "title": "Event Title",
    "host": "host_uuid",
    "track": "Track Name",
    "status": "open",
    "starts_at": "2023-01-01T10:00:00",
    "ends_at": "2023-01-01T12:00:00",
    "drivers": [
      {
        "id": "driver_uuid",
        "name": "Driver Name"
      }
    ],
    "schedule": [
      {
        "id": 1,
        "type": "practice",
        "nbr_of_laps": 10,
        "duration": "30 minutes"
      }
    ]
  }
]
```

### Get Event by ID

```
GET /api/events/{event_id}/
```

**Response:**

```json
{
  "id": "event_uuid",
  "title": "Event Title",
  "host": "host_uuid",
  "track": "Track Name",
  "status": "open",
  "starts_at": "2023-01-01T10:00:00",
  "ends_at": "2023-01-01T12:00:00",
  "drivers": [
    {
      "id": "driver_uuid",
      "name": "Driver Name"
    }
  ],
  "schedule": [
    {
      "id": 1,
      "type": "practice",
      "nbr_of_laps": 10,
      "duration": "30 minutes"
    }
  ]
}
```

### Create Event

```
POST /api/events/
```

**Request Body:**

```json
{
  "title": "New Event",
  "track": "Track Name",
  "starts_at": "2023-01-01T10:00:00",
  "ends_at": "2023-01-01T12:00:00"
}
```

**Response:**

```json
{
  "resource": "event_uuid"
}
```

### Join Event

```
PUT /api/events/{event_id}/join
```

**Response:**
204 No Content

### Leave Event

```
PUT /api/events/{event_id}/leave
```

**Response:**
204 No Content

## Event Schedules

### Add Event Schedule

```
POST /api/events/{event_id}/schedule
```

**Request Body:**

```json
{
  "type": "practice",
  "nbr_of_laps": 10,
  "duration": "30 minutes"
}
```

**Response:**
204 No Content

### Remove Event Schedule

```
DELETE /api/events/{event_id}/schedule/{schedule_id}
```

**Response:**
204 No Content

## Results

### Upload Event Results

```
POST /api/events/{event_id}/results
```

**Request:**
Multipart form data with a file field named "file".

**Response:**
204 No Content

### Upload Schedule Results

```
POST /api/events/{event_id}/schedule/{schedule_id}/results
```

**Request:**
Multipart form data with a file field named "file".

**Response:**
204 No Content

### Add Race Result

```
POST /api/events/{event_id}/result
```

**Request Body:**

```json
{
  "schedule_id": 1,
  "result": [
    {
      "driver_id": "driver_uuid",
      "position": 1,
      "fastest_lap": "1:23.456",
      "total_time": "30:45.678"
    }
  ]
}
```

**Response:**
204 No Content

## Error Handling

All API endpoints return standardized error responses in case of failure:

```json
{
  "code": 400,
  "message": "Error message",
  "error_type": "ErrorType"
}
```

In development mode, additional debug information may be included:

```json
{
  "code": 500,
  "message": "An unexpected error occurred",
  "error_type": "Exception",
  "debug_message": "Detailed error message"
}
```

For validation errors, the response includes field-specific error messages:

```json
{
  "code": 400,
  "message": "Validation error",
  "errors": {
    "field_name": "Error message for this field"
  }
}
```
