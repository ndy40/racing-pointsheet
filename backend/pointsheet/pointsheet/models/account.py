from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from pointsheet.domain import EntityId
from .base import BaseModel
from .custom_types import EntityIdType


class Driver(BaseModel):
    __tablename__ = "drivers"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        primary_key=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
