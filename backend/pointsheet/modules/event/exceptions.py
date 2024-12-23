from pointsheet.exceptions import PointSheetException


class SeriesNotFoundException(PointSheetException):
    code = 404
    message = "Series not found"


class EventAlreadyExists(PointSheetException):
    message = "Event already exists"
