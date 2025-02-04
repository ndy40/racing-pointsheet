from pointsheet.domain.exceptions.base import PointSheetException


class InvalidUserException(PointSheetException):
    message = "user not found"


class InvalidPassword(PointSheetException):
    pass


class UserAlreadyExists(PointSheetException):
    message = "user already exists"


class EventNotFoundException(PointSheetException):
    message = "event not found"
