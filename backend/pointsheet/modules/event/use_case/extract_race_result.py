from uuid import uuid4

import cv2
import pytesseract
from typing import Any, List, Optional

from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from pydantic import BaseModel, NonNegativeInt

from modules.event.domain.entity import RaceResult, Driver
from modules.event.domain.value_objects import DriverResult
from modules.event.repository import EventRepository
from pointsheet.langchain import vertex_ai


def get_text_from_image(file_path):
    img = cv2.imread(file_path)
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[
        1
    ]

    median = cv2.medianBlur(thresh, 5)
    return pytesseract.image_to_string(median)


class Result(BaseModel):
    position: NonNegativeInt
    driver: str
    best_lap: Optional[str] = None
    race: Optional[str] = None
    penalties: Optional[float] = None
    total: Optional[str] = None


class ListOfResults(BaseModel):
    results: List[Result]


class ExtractRaceResult:
    def __init__(self, image_path):
        self.image_path = image_path

    def execute(self) -> Any:
        system_prompt = SystemMessage(
            """
            You are a helpful assistant. Extract race results from the context. Response only with the requested output format. """
        )
        human_prompt = HumanMessagePromptTemplate.from_template(
            """Extract the race results from the context. Where you see ONF, replace with DNF. Fields position, driver, best_lap, race, penalties, total.
            Json response preferred -

            example:
            \"""{{ "results": [{{...}}]}}\"""

            Race Data:
            ------
            {context}

            """
        )

        chain = vertex_ai.create_system_prompt(
            system_prompt, human_prompt, response_model=ListOfResults
        )
        output = chain({"context": f"Image: {get_text_from_image(self.image_path)}"})
        return output


class SaveRaceResult:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def __call__(self, event_id, schedule_id, race_result: ListOfResults):
        if not race_result.results:
            return

        event = self.event_repo.find_by_id(event_id)
        driver_results = []

        for result in race_result.results:
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
            event.add_result(
                race_result=RaceResult(schedule_id=schedule_id, result=driver_results)
            )
            self.event_repo.update(event)
