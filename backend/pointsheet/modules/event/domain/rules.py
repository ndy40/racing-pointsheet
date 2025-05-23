from pydantic import BaseModel

from pointsheet.domain.rules import BusinessRule


class EventDatesIsWithinSeriesDates(BusinessRule):
    series: BaseModel
    event: BaseModel

    def is_broken(self) -> bool: ...
