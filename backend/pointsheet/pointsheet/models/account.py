from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from modules.account.domain.value_objects import TeamMember
from pointsheet.domain import EntityId
from .base import BaseModel
from .custom_types import EntityIdType, PydanticJsonType


class Team(BaseModel):
    __tablename__ = "teams"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    owner_id: Mapped[EntityId] = mapped_column(EntityIdType)
    members: Mapped[List[TeamMember]] = mapped_column(
        PydanticJsonType[TeamMember](TeamMember)
    )


class Driver(BaseModel):
    __tablename__ = "users"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        primary_key=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    team_id: Mapped[Optional[EntityId]] = mapped_column(EntityIdType, nullable=True)
