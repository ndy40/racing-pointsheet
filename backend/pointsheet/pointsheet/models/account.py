from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from pointsheet.domain.value_objects import TeamMember
from pointsheet.domain.types import EntityId
from .base import BaseModel
from .custom_types import EntityIdType, PydanticJsonType, UserRoleType
from ..domain.entity import UserRole


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
    __tablename__ = "drivers"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        primary_key=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    team_id: Mapped[Optional[EntityId]] = mapped_column(EntityIdType, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(UserRoleType, default=UserRole.driver)
