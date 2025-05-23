from typing import Optional

from pydantic import BaseModel, Field

from pointsheet.domain.types import EntityId, uuid_default


class AggregateRoot(BaseModel):
    id: Optional[EntityId] = Field(default_factory=uuid_default)
