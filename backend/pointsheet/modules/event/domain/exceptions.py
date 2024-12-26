from pointsheet.domain.exceptions import PointSheetException


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
