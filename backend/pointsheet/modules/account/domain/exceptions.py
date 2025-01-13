from pointsheet.domain.exceptions.base import PointSheetException


class AlreadySignedUpException(PointSheetException):
    message = "User already signed up"
