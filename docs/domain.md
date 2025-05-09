# Racing Pointsheet Domain Model

This document describes the domain model and business rules for the Racing Pointsheet application.

## Core Entities

### Event

An Event represents a racing event that users can participate in.

**Attributes:**

- `id`: Unique identifier for the event
- `title`: Title of the event
- `host`: User who created the event
- `track`: Track where the event takes place
- `status`: Current status of the event (open, closed, cancelled)
- `starts_at`: Start date and time of the event
- `ends_at`: End date and time of the event
- `drivers`: List of drivers participating in the event
- `schedule`: List of scheduled activities for the event

**Business Rules:**

- An event must have a title and a host
- If an end date is set, a start date must also be set
- The end date cannot be earlier than the start date
- A driver cannot join an event more than once

### Schedule

A Schedule represents a specific activity within an event, such as practice, qualification, or race.

**Attributes:**

- `id`: Unique identifier for the schedule
- `type`: Type of schedule (practice, qualification, race)
- `nbr_of_laps`: Number of laps for the schedule (optional)
- `duration`: Duration of the schedule (optional)
- `result`: Result of the schedule (optional)

**Business Rules:**

- An event can have only one schedule of type "practice"
- An event can have only one schedule of type "qualification"
- An event can have multiple schedules of type "race"
- Schedules are ordered by type: practice, qualification, race

### Driver

A Driver represents a user participating in an event.

**Attributes:**

- `id`: Unique identifier for the driver
- `name`: Name of the driver

### RaceResult

A RaceResult represents the outcome of a scheduled activity.

**Attributes:**

- `id`: Unique identifier for the result
- `schedule_id`: ID of the schedule this result belongs to
- `result`: List of driver results
- `mark_down`: Markdown text describing the result (optional)
- `upload_file`: Path to an uploaded file containing the result (optional)

**Business Rules:**

- A result can only be added to an existing schedule
- All driver results must be instances of DriverResult

### DriverResult

A DriverResult represents an individual driver's performance in a race.

**Attributes:**

- `driver_id`: ID of the driver
- `position`: Finishing position
- `fastest_lap`: Fastest lap time (optional)
- `total_time`: Total race time (optional)

### Series

A Series represents a collection of related events.

**Attributes:**

- `id`: Unique identifier for the series
- `title`: Title of the series
- `status`: Current status of the series (not_started, started, closed)
- `events`: List of events in the series
- `starts_at`: Start date and time of the series
- `ends_at`: End date and time of the series

**Business Rules:**

- A series can only be started if it's not already closed
- Events added to a series must have dates within the series' date range
- Events in a series are ordered by start date

### Track

A Track represents a racing circuit.

**Attributes:**

- `id`: Unique identifier for the track
- `name`: Name of the track
- `layout`: Layout of the track
- `country`: Country where the track is located
- `length`: Length of the track

## Value Objects

### EventStatus

Represents the possible states of an event:

- `open`: The event is open for registration
- `closed`: The event is closed for registration
- `cancelled`: The event has been cancelled

### ScheduleType

Represents the types of schedules:

- `practice`: Practice session
- `qualification`: Qualification session
- `race`: Race session

### SeriesStatus

Represents the possible states of a series:

- `not_started`: The series has not started yet
- `started`: The series is currently active
- `closed`: The series has ended

## Aggregates

The main aggregates in the system are:

1. **Event Aggregate**

   - Root: Event
   - Contains: Schedule, Driver, RaceResult, DriverResult

2. **Series Aggregate**
   - Root: Series
   - Contains: Event (references)

## Commands and Queries

The application follows the Command Query Responsibility Segregation (CQRS) pattern:

### Commands

Commands modify the state of the system:

- CreateEvent
- JoinEvent
- LeaveEvent
- AddEventSchedule
- RemoveSchedule
- AddEventResult
- UploadRaceResult

### Queries

Queries retrieve data without modifying state:

- GetEvent
- GetEvents
- GetAvailableEvents
- GetOngoingEvents
- GetRecentEvent
- GetAllTracks
- GetAllSeries
- GetSeriesById

## Exception Handling

The domain model includes specific exceptions for business rule violations:

- `InvalidEventDateForSeries`: Thrown when an event's dates are outside the series' date range
- `SeriesAlreadyClosed`: Thrown when attempting to start a series that is already closed
- `DriverAlreadySingedUp`: Thrown when a driver attempts to join an event they're already part of
