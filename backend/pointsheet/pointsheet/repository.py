import abc
from abc import abstractmethod
from typing import Any, Generic, List, TypeVar

from sqlalchemy import select

from pointsheet.domain.types import EntityId
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

    def __init__(self, session):
        self._session = session

    def add(self, model: T) -> None:
        entity: DbModel = self._map_to_entity(model)
        session = self._session
        session.add(entity)

    def update(self, model: T) -> None:
        entity: DbModel = self._map_to_entity(model)
        session = self._session
        session.merge(entity)

    @abstractmethod
    def delete(self, id: Any or EntityId) -> None: ...

    def all(self) -> List[T]:
        session = self._session
        stmt = select(DbModel).order_by(DbModel.id)
        result = session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result] if result else None


    @property
    def mapper(self):
        return self.mapper_class()

    def _map_to_entity(self, model: T) -> DbModel:
        assert self.mapper
        return self.mapper.to_db_entity(model)

    def _map_to_model(self, instance: DbModel) -> T:
        assert self.mapper
        return self.mapper.to_domain_model(instance)
