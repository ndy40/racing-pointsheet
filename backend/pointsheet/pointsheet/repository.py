import abc
from abc import abstractmethod
from typing import Any, Generic, List, TypeVar

from sqlalchemy import select

from pointsheet.domain import EntityId
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

    def __init__(self, db_session_factory):
        """
        Initialize with a session factory function.

        Args:
            db_session_factory: A function that returns a new database session
        """
        self._session_factory = db_session_factory

    @property
    def _session(self):
        """Get a session using the factory."""
        return (
            self._session_factory()
            if callable(self._session_factory)
            else self._session_factory
        )

    def add(self, model: T) -> None:
        entity: DbModel = self._map_to_entity(model)
        session = self._session
        try:
            session.add(entity)
            session.commit()
        finally:
            session.close()

    def update(self, model: T) -> None:
        entity: DbModel = self._map_to_entity(model)
        session = self._session
        try:
            session.merge(entity)
            session.commit()
        finally:
            session.close()

    @abstractmethod
    def delete(self, id: Any or EntityId) -> None: ...

    def all(self) -> List[T]:
        session = self._session
        try:
            stmt = select(DbModel).order_by(DbModel.id)
            result = session.execute(stmt).scalars()
            return [self._map_to_model(item) for item in result]
        finally:
            session.close()
        return None

    @property
    def mapper(self):
        return self.mapper_class()

    def _map_to_entity(self, model: T) -> DbModel:
        assert self.mapper
        return self.mapper.to_db_entity(model)

    def _map_to_model(self, instance: DbModel) -> T:
        assert self.mapper
        return self.mapper.to_domain_model(instance)
