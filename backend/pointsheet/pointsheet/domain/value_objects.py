from datetime import datetime

from pydantic import BaseModel

from pointsheet.domain.types import EntityId


class TeamMember(BaseModel):
    driver_id: EntityId
    role: str  # e.g., "member"
    joined_at: datetime
