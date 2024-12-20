import abc
from abc import abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

from pointsheet.models import BaseModel

DbModel = TypeVar("S", bound=BaseModel)
T = TypeVar("T", bound="Any")


class DataMapper(Generic[DbModel, T], abc.ABC):
    entity_class: type[DbModel]
    model_class: type[T]

    @abstractmethod
    def to_entity(self, instance: DbModel) -> T:
        raise NotImplementedError

    @abstractmethod
    def to_model(self, instance: T) -> DbModel:
        raise NotImplementedError


class AbstractRepository(Generic[DbModel, T], abc.ABC):
    mapper_class: type[DataMapper[DbModel, T]]
    model_class: type[T]

    def __init__(self, db_session: Session):
        self._session = db_session

    def add(self, model: T) -> None:
        entity = self._map_to_entity(model)
        self._session.add(entity)

    @abstractmethod
    def find_by_id(self, id: Any) -> T | None: ...

    @property
    def mapper(self):
        return self.mapper_class()

    def _map_to_entity(self, model: T) -> DbModel:
        assert self.mapper
        return self.mapper.to_model(model)

    def _map_to_model(self, instance: DbModel) -> T:
        assert self.mapper
        return self.mapper.to_model(instance)
