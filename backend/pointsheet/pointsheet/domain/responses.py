from pydantic import BaseModel


class ResourceCreated(BaseModel):
    resource: str
