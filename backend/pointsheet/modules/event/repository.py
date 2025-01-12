from typing import Any, List

from lato import Query
from sqlalchemy import select

from pointsheet.models import Event, Series
from pointsheet.repository import AbstractRepository

from .data_mappers import EventModelMapper, SeriesModelMapper
from .domain.entity import Event as EventModel
from .domain.entity import Series as SeriesModel
from pointsheet.domain import EntityId


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> EventModel | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)

    def all(self) -> List[EventModel]:
        stmt = select(Event).order_by(Event.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Event.id, id)
        self._session.delete(entity_to_delete)
        self._session.commit()


class SeriesRepository(AbstractRepository[Series, SeriesModel]):
    mapper_class = SeriesModelMapper
    model_class = SeriesModel

    def all(self, criteria: Query) -> List[SeriesModel]:
        """

        :param criteria: Query -
            Supported filtering parameters
            fields:
            status: Open, Closed, None, using == check. None filters everything.
        :return: List[SeriesModel]
        """
        stmt = select(Series).order_by(Series.id)

        if value := getattr(criteria, "status"):
            stmt = stmt.where(Series.status == value.value)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: Any) -> SeriesModel | None:
        result = self._session.get(Series, id)

        if result:
            return self._map_to_model(result)

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Series, id)
        self._session.delete(entity_to_delete)
        self._session.commit()
