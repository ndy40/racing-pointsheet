from pointsheet.domain.exceptions.base import PointSheetException


class SeriesNotFoundException(PointSheetException):
    code = 404
    message = "Home not found"


class EventAlreadyExists(PointSheetException):
    message = "Event already exists"


class SeriesAlreadyClosed(PointSheetException):
    code = 400
    message = "Home can't be started after being closed"


class InvalidEventDateForSeries(PointSheetException):
    message = "Event date not within series start and end date range"
    code = 400


class DriverAlreadySingedUp(PointSheetException):
    message = "Driver already signed up to event"
    code = 400


class DriverNotFound(PointSheetException):
    message = "Driver not found"
    code = 404


class DuplicatePositionInRaceResult(PointSheetException):
    message = "Duplicate position in race result"
    code = 400


class DuplicateDriverInRaceResult(PointSheetException):
    message = "Duplicate driver in race result"
    code = 400

class HostNotFound(PointSheetException):
    message = "Host not found"
    code = 404

class NoCarFound(PointSheetException):
    message = "Car not found"
    code = 404