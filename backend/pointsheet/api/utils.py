from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadSignature

from modules.auth.auth import TimedSerializer
from pointsheet.domain.exceptions.base import PointSheetException

auth = HTTPTokenAuth(scheme="Bearer")


class _AuthenticationException(PointSheetException):
    message = "Authentication failed"


@auth.verify_token
def verify_token(token):
    try:
        result = TimedSerializer().deserializer(token)
        return result[0]
    except BadSignature:
        raise _AuthenticationException()
