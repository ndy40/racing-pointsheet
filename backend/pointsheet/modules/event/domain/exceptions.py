from pointsheet.domain.exceptions.base import PointSheetException


class SeriesNotFoundException(PointSheetException):
    code = 404
    message = "Series not found"


class EventAlreadyExists(PointSheetException):
    message = "Event already exists"


class SeriesAlreadyClosed(PointSheetException):
    code = 400
    message = "Series can't be started after being closed"


class InvalidEventDateForSeries(PointSheetException):
    message = "Event date not within series start and end date range"
    code = 400


class DriverAlreadySingedUp(PointSheetException):
    message = "Driver already signed up to event"
    code = 400


class DriverNotFound(PointSheetException):
    message = "Driver not found"
    code = 404
