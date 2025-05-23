from typing import Union, List
from uuid import uuid4

from modules.event.domain.entity import Driver, RaceResult
from modules.event.domain.value_objects import ListOfResults, Result, DriverResult
from modules.event.repository import EventRepository


class SaveRaceResult:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def __call__(
        self, event_id, schedule_id, race_result: Union[ListOfResults | List[Result]]
    ):
        results = (
            race_result.results
            if isinstance(race_result, ListOfResults)
            else race_result
        )

        if not results:
            return

        event = self.event_repo.find_by_id(event_id)
        driver_results = []

        for result in results:
            driver = event.find_driver_by_id_or_name(result.driver_id or result.driver)
            if not driver:
                driver = Driver(id=uuid4(), name=result.driver)
                event.add_driver(driver)

            driver_result = DriverResult(
                driver_id=driver.id,
                driver=driver.name,
                position=result.position,
                best_lap=result.best_lap,
                total=result.total,
            )

            driver_results.append(driver_result)

        if driver_results:
            race_result = RaceResult(schedule_id=schedule_id)
            race_result.add_result(*driver_results)
            event.add_result(race_result=race_result)
            self.event_repo.update(event)
