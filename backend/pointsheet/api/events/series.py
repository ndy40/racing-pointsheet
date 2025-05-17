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
from pointsheet.auth import api_auth
from pointsheet.domain import EntityId
from modules.event.queries.get_all_series import GetAllSeries
from modules.event.queries.get_series_by_id import GetSeriesById
from pointsheet.domain.responses import ResourceCreated


series_bp = Blueprint("event", __name__)


@series_bp.route("/series", methods=["GET"])
@api_auth.login_required
def fetch_all_series():
    cmd = GetAllSeries(**request.args.to_dict())
    result = current_app.application.execute(cmd)
    return [item.model_dump() for item in result]


@series_bp.route("/series", methods=["POST"])
@api_auth.login_required
def create_series():
    try:
        cmd = CreateSeries(**request.json)
        current_app.application.execute(cmd)
        series: Series = current_app.application.execute(GetSeriesById(id=cmd.id))
        return ResourceCreated(resource=str(series.id)).model_dump(), 201
    except ValueError as e:
        return {"error": str(e)}, 400


@series_bp.route("/series/<uuid:series_id>/status", methods=["PUT"])
@api_auth.login_required
def update_series_status(series_id):
    try:
        cmd = UpdateSeriesStatus(series_id=series_id, status=request.json.get("status"))
        current_app.application.execute(cmd)
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@series_bp.route("/series/<uuid:series_id>", methods=["DELETE"])
@api_auth.login_required
def delete_series(series_id):
    try:
        current_app.application.execute(DeleteSeries(id=series_id))
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.NOT_FOUND


@series_bp.route("/series/<uuid:series_id>", methods=["GET"])
@api_auth.login_required
def fetch_series_by_id(series_id):
    cmd = GetSeriesById(id=series_id)
    series: Series = current_app.application.execute(cmd)

    if series:
        return series.model_dump()

    return Response(status=HTTPStatus.NOT_FOUND)


@series_bp.route("/series/<uuid:series_id>/events", methods=["POST"])
@api_auth.login_required
def create_event_for_series(series_id):
    try:
        cmd = CreateEventForSeries(series_id=series_id, event=Event(**request.json))
        current_app.application.execute(cmd)
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@series_bp.route("/series/<uuid:series_id>/events", methods=["PUT"])
@api_auth.login_required
def update_event_for_series(series_id: EntityId):
    try:
        cmd = UpdateSeriesEvent(
            series_id=series_id, event=UpdateEventModel(**request.json)
        )
        current_app.application.execute(cmd)
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@series_bp.route("/series/<uuid:series_id>/events/<uuid:event_id>/", methods=["DELETE"])
@api_auth.login_required
def delete_series_event(series_id, event_id):
    try:
        cmd = DeleteSeriesEvent(series_id=series_id, event_id=event_id)
        current_app.application.execute(cmd)
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.NOT_FOUND
