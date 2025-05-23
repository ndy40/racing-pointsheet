import warnings
from sqlalchemy.orm import DeclarativeBase
from pointsheet.domain.types import uuid_default as _uuid_default


class BaseModel(DeclarativeBase):
    pass


def uuid_default():
    warnings.warn(
        "Importing uuid_default from pointsheet.models.base is deprecated. "
        "Import from pointsheet.domain.types instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _uuid_default()
