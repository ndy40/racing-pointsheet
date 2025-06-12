from typing import List

from pydantic import BaseModel

from pointsheet.domain.entity import UserRole
from pointsheet.domain.types import EntityId


class DriverResponse(BaseModel):
    """
    Response model for a single driver.
    Contains the driver's id, name, and role.
    """
    id: EntityId
    name: str
    role: UserRole | None = None


class DriversResponse(BaseModel):
    """
    Response model for the GET /api/account/drivers endpoint.
    Contains a list of drivers.
    """
    drivers: List[DriverResponse]