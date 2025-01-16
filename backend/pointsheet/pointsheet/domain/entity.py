from typing import Optional

from pydantic import BaseModel

from pointsheet.domain import EntityId


class AggregateRoot(BaseModel):
    id: Optional[EntityId] = None
