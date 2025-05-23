from pointsheet.domain.exceptions.base import PointSheetException


class AlreadySignedUpException(PointSheetException):
    message = "User already signed up"


class AlreadyTeamMemberException(PointSheetException):
    message = "Driver is already a member of this team"


class AlreadyInTeamException(PointSheetException):
    message = "Driver is already a member of a team"


class NotTeamMemberException(PointSheetException):
    message = "Driver is not a member of this team"


class NotTeamOwnerException(PointSheetException):
    message = "User is not the owner of this team"
