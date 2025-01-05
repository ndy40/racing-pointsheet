from typing import Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, validates

from modules.account.domain.entity import UserRole
from pointsheet.domain import EntityId
from pointsheet.models import BaseModel, EntityIdType
from pointsheet.models.base import uuid_default
from pointsheet.models.custom_types import UserRoleType


class User(BaseModel):
    __tablename__ = "user_account"

    id: Mapped[EntityId] = mapped_column(
        EntityIdType, primary_key=True, default=uuid_default
    )
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Optional[str]] = mapped_column(UserRoleType, default=UserRole.driver)
    is_active = mapped_column(Boolean, default=False)
    last_login = mapped_column(DateTime, nullable=True)
    auth_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    auth_expires_in: Mapped[Optional[str]] = mapped_column(DateTime, nullable=True)

    @validates("auth_expires_in")
    def validate_auth_expires_in(self, key, value):
        if self.auth_token and not value:
            raise ValueError("auth_expires_in required if auth_token is set")
