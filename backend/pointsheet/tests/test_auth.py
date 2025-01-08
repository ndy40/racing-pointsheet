from pointsheet import config
from pointsheet.auth import TimedSerializer


def test_serialize_works():
    serializer = TimedSerializer(config.AUTH_TOKEN_MAX_AGE)
    data = serializer.serialize("random_string")
    assert isinstance(data, str)
