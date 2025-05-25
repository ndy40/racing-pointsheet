from http import HTTPStatus

from flask import Blueprint, Response, current_app, request, jsonify

from modules.event.commands.create_series import CreateSeries
from modules.event.commands.create_series_event import CreateEventForSeries
from modules.event.commands.delete_series import DeleteSeries
from modules.event.commands.delete_series_event import DeleteSeriesEvent
from modules.event.commands.update_series import UpdateSeries
from modules.event.commands.update_series_event import (
    UpdateEventModel,
    UpdateSeriesEvent,
)
from modules.event.commands.update_series_status import UpdateSeriesStatus
from modules.event.commands.upload_series_cover_image import UploadSeriesCoverImage
from modules.event.domain.entity import Event, Series
from pointsheet.auth import api_auth
from pointsheet.domain.types import EntityId
from modules.event.queries.get_all_series import GetAllSeries
from modules.event.queries.get_series_by_id import GetSeriesById
from pointsheet.domain.responses import ResourceCreated
from utils.file_validation import validate_file, secure_filename


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


@series_bp.route("/series/<uuid:series_id>", methods=["PATCH"])
@api_auth.login_required
def update_series(series_id):
    try:
        cmd = UpdateSeries(series_id=series_id, **request.json)
        current_app.application.execute(cmd)
        return ResourceCreated(resource=str(series_id)).model_dump(), HTTPStatus.OK
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


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


@series_bp.route("/series/<uuid:series_id>/cover-image", methods=["POST"])
@api_auth.login_required
def upload_series_cover_image(series_id):
    try:
        uploaded_file = request.files.get("image")
        allowed_extensions = {"jpg", "jpeg", "png"}

        # Validate the file
        is_valid, error_message = validate_file(uploaded_file, allowed_extensions)
        if not is_valid:
            return jsonify({"error": error_message}), HTTPStatus.BAD_REQUEST

        # Generate a secure filename
        secure_filename(uploaded_file.filename)

        # Create and execute the command
        cmd = UploadSeriesCoverImage(series_id=series_id, file=uploaded_file)
        current_app.application.execute(cmd)

        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@series_bp.route("/series/<uuid:series_id>/events/<uuid:event_id>/", methods=["DELETE"])
@api_auth.login_required
def delete_series_event(series_id, event_id):
    try:
        cmd = DeleteSeriesEvent(series_id=series_id, event_id=event_id)
        current_app.application.execute(cmd)
        return Response(status=HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.NOT_FOUND
