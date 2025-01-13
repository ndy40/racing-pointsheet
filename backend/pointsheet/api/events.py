import logging
from http import HTTPStatus

from flask import Blueprint, Response, current_app, request

from modules.event.commands.create_series import CreateSeries
from modules.event.commands.create_series_event import CreateEventForSeries
from modules.event.commands.delete_series import DeleteSeries
from modules.event.commands.delete_series_event import DeleteSeriesEvent
from modules.event.commands.update_series_event import (
    UpdateEventModel,
    UpdateSeriesEvent,
)
from modules.event.commands.update_series_status import UpdateSeriesStatus
from modules.event.domain.entity import Event, Series
from pointsheet.domain import EntityId
from modules.event.queries.get_all_series import GetAllSeries
from modules.event.queries.get_series_by_id import GetSeriesById

from .utils import auth

logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

event_bp = Blueprint("event", __name__)


@event_bp.route("/series", methods=["GET"])
@auth.login_required
def fetch_all_series():
    cmd = GetAllSeries(**request.args.to_dict())
    result = current_app.application.execute(cmd)
    return [item.model_dump() for item in result]


@event_bp.route("/series", methods=["POST"])
@auth.login_required
def create_series():
    cmd = CreateSeries(**request.json)
    current_app.application.execute(cmd)
    series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))
    return series.model_dump()


@event_bp.route("/series/<uuid:series_id>/status", methods=["PUT"])
@auth.login_required
def update_series_status(series_id):
    cmd = UpdateSeriesStatus(series_id=series_id, status=request.json.get("status"))
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>", methods=["DELETE"])
@auth.login_required
def delete_series(series_id):
    current_app.application.execute(DeleteSeries(id=series_id))
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>", methods=["GET"])
@auth.login_required
def fetch_series_by_id(series_id):
    cmd = GetSeriesById(id=series_id)
    series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))

    if series:
        return series.model_dump()

    return Response(status=HTTPStatus.NOT_FOUND)


@event_bp.route("/series/<uuid:series_id>/events", methods=["POST"])
@auth.login_required
def create_event_for_series(series_id):
    cmd = CreateEventForSeries(series_id=series_id, event=Event(**request.json))
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>/events", methods=["PUT"])
@auth.login_required
def update_event_for_series(series_id: EntityId):
    cmd = UpdateSeriesEvent(series_id=series_id, event=UpdateEventModel(**request.json))
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)


@event_bp.route("/series/<uuid:series_id>/events/<uuid:event_id>/", methods=["DELETE"])
@auth.login_required
def delete_series_event(series_id, event_id):
    cmd = DeleteSeriesEvent(series_id=series_id, event_id=event_id)
    current_app.application.execute(cmd)
    return Response(status=HTTPStatus.NO_CONTENT)
