from time import sleep

import pytest
from itsdangerous import SignatureExpired

from pointsheet.auth import TimedSerializer
from pointsheet.config import config


def test_serialize_works():
    serializer = TimedSerializer(config.AUTH_TOKEN_MAX_AGE)
    data = serializer.serialize("random_string")
    assert isinstance(data, str)


def test_time_serializer_failed_on_expired_token():
    serializer = TimedSerializer(1)
    data = serializer.serialize("random_string")
    sleep(3)
    with pytest.raises(SignatureExpired):
        serializer.deserializer(data)
