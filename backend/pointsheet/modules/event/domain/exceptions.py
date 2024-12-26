from pointsheet.domain.exceptions import PointSheetException


class SeriesNotFoundException(PointSheetException):
    code = 404
    message = "Series not found"


class EventAlreadyExists(PointSheetException):
    message = "Event already exists"


class InvalidEventDateForSeries(PointSheetException):
    message = "Event date not within series start and end date range"
