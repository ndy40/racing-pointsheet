import logging
from http import HTTPStatus

from flask import Blueprint, Response, current_app, request

from modules.event.commands.create_series import CreateSeries
from modules.event.commands.create_series_event import CreateSeriesEvent
from modules.event.commands.delete_series import DeleteSeries
from modules.event.commands.update_series_event import (
    UpdateEventModel,
    UpdateSeriesEvent,
)
from modules.event.domain.entity import Event, Series
from modules.event.domain.value_objects import EntityId
from modules.event.queries.get_all_series import GetAllSeries
from modules.event.queries.get_series_by_id import GetSeriesById

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

event_bp = Blueprint("event", __name__)


@event_bp.route("/series", methods=["GET"])
def fetch_all_series():
    cmd = GetAllSeries(**request.args.to_dict())
    result = current_app.application.execute(cmd)
    return [item.model_dump() for item in result]


@event_bp.route("/series", methods=["POST"])
def create_series():
    cmd = CreateSeries(**request.json)
    current_app.application.execute(cmd)
    series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))
    return series.model_dump()


@event_bp.route("/series/<uuid:series_id>", methods=["DELETE"])
def delete_series(series_id):
    current_app.application.execute(DeleteSeries(id=series_id))
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>", methods=["GET"])
def fetch_series_by_id(series_id):
    cmd = GetSeriesById(id=series_id)
    series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))

    if series:
        return series.model_dump()

    return Response(status=HTTPStatus.NOT_FOUND)


@event_bp.route("/series/<uuid:series_id>/events", methods=["POST"])
def create_event_for_series(series_id: EntityId):
    cmd = CreateSeriesEvent(series_id=series_id, event=Event(**request.json["event"]))
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>/events", methods=["PUT"])
def update_event_for_series(series_id: EntityId):
    cmd = UpdateSeriesEvent(series_id=series_id, event=UpdateEventModel(**request.json))
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)
