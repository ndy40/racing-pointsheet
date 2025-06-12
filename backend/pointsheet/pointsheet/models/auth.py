from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..domain.entity import EntityId, UserRole
from .base import BaseModel
from pointsheet.models.custom_types import UserRoleType, EntityIdType


class User(BaseModel):
    __tablename__ = "user_account"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(Text)
    role: Mapped[Optional[str]] = mapped_column(UserRoleType, default=UserRole.driver)
    is_active = mapped_column(Boolean, default=False)
    last_login = mapped_column(DateTime, nullable=True)
    auth_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    auth_expires_in: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    registered_on: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    @validates("auth_expires_in")
    def validate_auth_expires_in(self, key, value):
        if self.auth_token and not value:
            raise ValueError("auth_expires_in required if auth_token is set")

        return value
