import uuid

from sqlalchemy.orm import Mapped, mapped_column

from event.domain.value_objects import EntityId
from pointsheet.models import BaseModel, SeriesStatusType
from pointsheet.models.custom_types import EntityIdType


def uuid_default():
    return str(uuid.uuid4())


class Series(BaseModel):
    __tablename__ = "series"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    title: Mapped[str]
    status: Mapped[str] = mapped_column(SeriesStatusType)


class Event(BaseModel):
    __tablename__ = "events"
    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    title: Mapped[str]
