from typing import Optional

from pydantic import BaseModel

from pointsheet.domain import EntityId
from pointsheet.domain.mixins import BusinessRuleValidationMixin


class AggregateRoot(BusinessRuleValidationMixin, BaseModel):
    id: Optional[EntityId] = None
