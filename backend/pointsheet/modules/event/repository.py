from datetime import datetime, timezone
from typing import Any, List, Union

from lato import Query
from sqlalchemy import select, or_, func

from pointsheet.models import Event, Series, Participants, Track, Car, Game
from pointsheet.repository import AbstractRepository
from pointsheet.domain.responses import PaginatedResponse

from .data_mappers import EventModelMapper, SeriesModelMapper, TrackModelMapper, CarModelMapper, GameModelMapper
from .domain.entity import Event as EventModel
from .domain.entity import Series as SeriesModel
from .domain.entity import Track as TrackModel
from .domain.entity import Car as CarModel
from .domain.entity import Game as GameModel
from pointsheet.domain.types import EntityId
from .domain.value_objects import EventStatus


class EventRepository(AbstractRepository[Event, EventModel]):
    mapper_class = EventModelMapper
    model_class = EventModel

    def find_by_id(self, id: Any) -> EventModel | None:
        stmt = select(Event).where(Event.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
        return None

    def all(self) -> List[EventModel]:
        stmt = select(Event).order_by(Event.id)
        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Event.id, id)
        self._session.delete(entity_to_delete)
        self._session.commit()

    def get_recent_event_by_user(self, query: Query):
        driver_search = {"id": str(query.driver_id)}

        stmt = (
            select(Event)
            .where(Event.drivers.contains([driver_search]))
            .order_by(Event.starts_at.desc())
            .limit(1)
        )
        result = self._session.execute(stmt).scalar()
        return self._map_to_model(result) if result else None

    def get_available_events(self, query: Query = None):
        stmt = (
            select(Event)
            .where(
                Event.starts_at > datetime.now(timezone.utc),
                Event.status == EventStatus.open,
            )
            .order_by(Event.starts_at)
        )

        if query.user_id:
            stmt = stmt.outerjoin(Participants).where(
                or_(Participants.id != query.user_id, Participants.id.is_(None))
            )

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def get_ongoing_events(self, query: Query):
        stmt = (
            select(Event)
            .where(Event.status.in_([EventStatus.in_progress, EventStatus.open]))
            .order_by(Event.starts_at)
        )

        if query.user_id:
            stmt = stmt.join(Participants).where(Participants.id == str(query.user_id))

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]


class SeriesRepository(AbstractRepository[Series, SeriesModel]):
    mapper_class = SeriesModelMapper
    model_class = SeriesModel

    def all(self, criteria: Query) -> List[SeriesModel]:
        stmt = select(Series).order_by(Series.id)

        if value := getattr(criteria, "status"):
            if isinstance(value, list):
                # Filter by multiple statuses
                status_values = [status.value for status in value]
                stmt = stmt.where(Series.status.in_(status_values))
            else:
                # Backward compatibility for single status
                stmt = stmt.where(Series.status == value.value)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: Any) -> SeriesModel | None:
        result = self._session.get(Series, id)

        if result:
            return self._map_to_model(result)
        return None

    def delete(self, id: EntityId) -> None:
        entity_to_delete = self._session.get(Series, id)
        self._session.delete(entity_to_delete)
        self._session.commit()


class TrackRepository(AbstractRepository[Track, TrackModel]):
    mapper_class = TrackModelMapper
    model_class = TrackModel

    def all(self, order: Query = None) -> List[TrackModel]:
        stmt = select(Track)

        if order:
            match (order.order_by.value, order.direction.value):
                case ("id", "asc"):
                    stmt = stmt.order_by(Track.id)
                case ("id", "desc"):
                    stmt = stmt.order_by(Track.id.desc())
                case ("name", "asc"):
                    stmt = stmt.order_by(Track.name)
                case ("name", "desc"):
                    stmt = stmt.order_by(Track.name.desc())
                case _:
                    pass

        else:
            stmt = stmt.order_by(Track.id)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: int) -> TrackModel | None:
        stmt = select(Track).where(Track.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
        return None


    def delete(self, id: Any or EntityId) -> None:
        pass


    def exists(self, id: int) -> bool:
        stmt = select(Track).where(Track.id == id)
        result = self._session.execute(stmt).scalar()
        return result is not None


class CarRepository(AbstractRepository[Car, CarModel]):
    mapper_class = CarModelMapper
    model_class = CarModel

    def _build_base_query(self) -> Any:
        """Build the base query for cars with game join."""
        return select(Car).join(Game)

    def _apply_game_filter(self, stmt: Any, query: Query = None) -> Any:
        """Apply game filter to the query if provided."""
        if query and hasattr(query, 'game_id') and query.game_id:
            # Check if game is an integer (id) or string (name)
            if isinstance(query.game_id, int):
                return stmt.where(Game.id == query.game_id)
            else:
                return stmt.where(Game.name == query.game)
        return stmt

    def _get_car_ids_from_search(self, search_term: str) -> List[int]:
        """Get car IDs that match the search term using FTS5."""
        from sqlalchemy import text
        try:
            # For content tables, join FTS5 results with the content table
            fts_stmt = select(text("cars.id")).select_from(
                text("car_fts").join(text("cars"), text("car_fts.rowid = cars.id"))
            ).where(text("car_fts MATCH :search")).params(search=search_term)

            return self._session.execute(fts_stmt).scalars().all()
        except Exception as e:
            # Log the error and return empty list to trigger fallback
            print(f"FTS5 search failed: {e}")
            return []

    def _apply_search_filter(self, stmt: Any, query: Query = None) -> Any:
        """Apply search filter to the query if provided."""
        if query and hasattr(query, 'search') and query.search:
            car_ids = self._get_car_ids_from_search(query.search)
            if car_ids:
                return stmt.where(Car.id.in_(car_ids))
            else:
                # Fallback to LIKE search if no FTS matches or if FTS is not available
                search_term = f"%{query.search}%"
                return stmt.where(Car.model.ilike(search_term))
        return stmt

    def _get_pagination_params(self, query: Query = None) -> tuple[int, int]:
        """Extract pagination parameters from the query."""
        page = 1
        page_size = 20

        if query:
            if hasattr(query, 'page'):
                page = max(1, query.page)  # Ensure page is at least 1
            if hasattr(query, 'page_size'):
                page_size = max(1, query.page_size)  # Ensure page_size is at least 1

        return page, page_size

    def _apply_pagination(self, stmt: Any, page: int, page_size: int) -> Any:
        """Apply pagination to the query."""
        return stmt.offset((page - 1) * page_size).limit(page_size)

    def _count_total_records(self, query: Query = None) -> int:
        """Count total records for pagination."""
        count_stmt = select(func.count()).select_from(Car).join(Game)
        count_stmt = self._apply_game_filter(count_stmt, query)
        count_stmt = self._apply_search_filter(count_stmt, query)
        return self._session.execute(count_stmt).scalar() or 0

    def all(self, query: Query = None) -> Union[List[CarModel], PaginatedResponse[CarModel]]:
        """Get all cars with optional filtering, searching, and pagination."""
        # Build base query
        stmt = self._build_base_query()

        # Apply filters
        stmt = self._apply_game_filter(stmt, query)
        stmt = self._apply_search_filter(stmt, query)

        # Order by id by default
        stmt = stmt.order_by(Car.id)

        # Get total count for pagination
        total = self._count_total_records(query)

        # Apply pagination
        page, page_size = self._get_pagination_params(query)
        stmt = self._apply_pagination(stmt, page, page_size)

        # Execute query and map results
        result = self._session.execute(stmt).scalars()
        items = [self._map_to_model(item) for item in result]

        # Create and return paginated response
        return PaginatedResponse.create(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )

    def find_by_id(self, id: int) -> CarModel | None:
        stmt = select(Car).where(Car.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
        return None

    def delete(self, id: Any) -> None:
        entity_to_delete = self._session.get(Car, id)
        if entity_to_delete:
            self._session.delete(entity_to_delete)
            self._session.commit()

    def exists(self, id: int) -> bool:
        stmt = select(Car).where(Car.id == id)
        result = self._session.execute(stmt).scalar()
        return result is not None


class GameRepository(AbstractRepository[Game, GameModel]):
    mapper_class = GameModelMapper
    model_class = GameModel

    def all(self, query: Query = None) -> List[GameModel]:
        stmt = select(Game)

        # Order by id by default
        stmt = stmt.order_by(Game.id)

        result = self._session.execute(stmt).scalars()
        return [self._map_to_model(item) for item in result]

    def find_by_id(self, id: int) -> GameModel | None:
        stmt = select(Game).where(Game.id == id)
        result = self._session.execute(stmt).scalar()

        if result:
            return self._map_to_model(result)
        return None

    def delete(self, id: Any) -> None:
        entity_to_delete = self._session.get(Game, id)
        if entity_to_delete:
            self._session.delete(entity_to_delete)
            self._session.commit()

    def exists(self, id: int) -> bool:
        stmt = select(Game).where(Game.id == id)
        result = self._session.execute(stmt).scalar()
        return result is not None
