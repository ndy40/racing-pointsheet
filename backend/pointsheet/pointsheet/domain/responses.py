from pydantic import BaseModel

from pointsheet.domain.types import EntityId


class ResourceCreated(BaseModel):
    resource: str | EntityId
