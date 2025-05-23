import cv2
import pytesseract
from typing import Any

from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

from modules.event.domain.value_objects import ListOfResults
from pointsheet.langchain import vertex_ai


def get_text_from_image(file_path):
    img = cv2.imread(file_path)
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[
        1
    ]

    median = cv2.medianBlur(thresh, 5)
    return pytesseract.image_to_string(median)


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
