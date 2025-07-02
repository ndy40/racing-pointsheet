from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from pointsheet.domain.entity import UserRole
from pointsheet.domain.types import EntityId


class CurrentUserResponse(BaseModel):
    """
    Response model for the GET /api/auth endpoint.
    Contains information about the currently authenticated user.
    """
    id: EntityId
    username: str
    role: UserRole
    auth_expires_in: Optional[datetime] = None
