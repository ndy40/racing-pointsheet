from pointsheet.exceptions import PointSheetException


class SeriesNotFoundException(PointSheetException):
    message = "Series not found"


class EventAlreadyExists(PointSheetException):
    message = "Event already exists"
