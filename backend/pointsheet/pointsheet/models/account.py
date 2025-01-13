from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from pointsheet.domain import EntityId
from pointsheet.models import BaseModel, EntityIdType
from pointsheet.models.base import uuid_default


class Driver(BaseModel):
    __tablename__ = "driver"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    name: Mapped[Optional[str]] = None
