from abc import abstractmethod, ABC

from pydantic import BaseModel


class BusinessRule(BaseModel, ABC):
    __message = "Business rule broken"

    def get_message(self) -> str:
        return self.__message

    @abstractmethod
    def is_broken(self) -> bool:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"
