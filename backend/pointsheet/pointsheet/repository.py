import abc
from abc import abstractmethod
from typing import Any, Generic, List, TypeVar

from sqlalchemy.orm import Session

from pointsheet.models import BaseModel

DbModel = TypeVar("S", bound=BaseModel)
T = TypeVar("T", bound="Any")


class DataMapper(Generic[DbModel, T], abc.ABC):
    db_entity_class: type[DbModel]
    domain_model_class: type[T]

    @abstractmethod
    def to_db_entity(self, instance: DbModel) -> T:
        raise NotImplementedError

    @abstractmethod
    def to_domain_model(self, instance: DbModel) -> T:
        raise NotImplementedError


class AbstractRepository(Generic[DbModel, T], abc.ABC):
    mapper_class: type[DataMapper[DbModel, T]]
    model_class: type[T]

    def __init__(self, db_session: Session):
        self._session = db_session

    def add(self, model: T) -> None:
        entity: DbModel = self._map_to_entity(model)
        print("entity ", entity.title)
        self._session.add(entity)

    @abstractmethod
    def all(self) -> List[T]: ...

    @abstractmethod
    def find_by_id(self, id: Any) -> T | None: ...

    @property
    def mapper(self):
        return self.mapper_class()

    def _map_to_entity(self, model: T) -> DbModel:
        assert self.mapper
        return self.mapper.to_db_entity(model)

    def _map_to_model(self, instance: DbModel) -> T:
        assert self.mapper
        return self.mapper.to_domain_model(instance)
