from pydantic import BaseModel

from pointsheet.domain import EntityId


class ResourceCreated(BaseModel):
    resource: str | EntityId
