from flask import Blueprint, request, current_app, Response, jsonify

from modules.event.commands.add_event_schedule import AddEventSchedule
from modules.event.commands.add_race_result import AddEventResult
from modules.event.commands.create_event import CreateEvent
from modules.event.commands.join_event import JoinEvent
from modules.event.commands.leave_event import LeaveEvent
from modules.event.commands.remove_schedule import RemoveSchedule
from modules.event.commands.save_race_result import SaveEventResults
from modules.event.commands.save_uploaded_result import UploadRaceResult
from modules.event.queries.get_event import GetEvent
from modules.event.queries.get_events import GetEvents
from pointsheet.auth import api_auth, get_user_id
from pointsheet.domain.responses import ResourceCreated

event_bp = Blueprint("events", __name__)


@event_bp.route("/events/", methods=["POST"])
@api_auth.login_required
def events():
    cmd = CreateEvent(**request.json)
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=cmd.id))
    return ResourceCreated(resource=str(event.id)).model_dump(), 201


@event_bp.route("/events/", methods=["GET"])
@api_auth.login_required
def get_events():
    cmd = GetEvents()
    all_events = current_app.application.execute(cmd)
    return [evt.model_dump() for evt in all_events] if all_events else []


@event_bp.route("/events/<uuid:event_id>/", methods=["GET"])
@api_auth.login_required
def get_event(event_id):
    query = GetEvent(event_id=event_id)
    event = current_app.application.execute(query)
    return (event.model_dump(), 200) if event else Response(status=404)


@event_bp.route("/events/<uuid:event_id>/join", methods=["PUT"])
@api_auth.login_required
def join_event(event_id):
    cmd = JoinEvent(event_id=event_id, driver_id=get_user_id().id)
    current_app.application.execute(cmd)
    return Response(status=204)


@event_bp.route("/events/<uuid:event_id>/leave", methods=["PUT"])
@api_auth.login_required
def leave_event(event_id):
    cmd = LeaveEvent(event_id=event_id, driver_id=get_user_id().id)
    current_app.application.execute(cmd)
    return Response(status=204)


@event_bp.route(
    "/events/<uuid:event_id>/results",
    methods=["POST"],
)
@api_auth.login_required
def upload_results(event_id):
    from utils.file_validation import validate_file, secure_filename

    uploaded_file = request.files.get("file")
    allowed_extensions = {"csv", "jpg", "jpeg", "png"}

    # Validate the file
    is_valid, error_message = validate_file(uploaded_file, allowed_extensions)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Generate a secure filename
    secure_name = secure_filename(uploaded_file.filename)

    # Assuming there's a command like SaveEventResults to handle file uploads
    cmd = SaveEventResults(event_id=event_id, file=uploaded_file, filename=secure_name)
    current_app.application.execute(cmd)
    return Response(status=204)


@event_bp.route("/events/<uuid:event_id>/schedule", methods=["POST"])
@api_auth.login_required
def add_event_schedule(event_id):
    try:
        cmd = AddEventSchedule(event_id=event_id, **request.json)
        current_app.application.execute(cmd)
        return Response(status=204)
    except ValueError as e:
        return {"error": str(e)}, 400


@event_bp.route(
    "/events/<uuid:event_id>/schedule/<int:schedule_id>", methods=["DELETE"]
)
@api_auth.login_required
def remove_event_schedule(event_id, schedule_id):
    try:
        cmd = RemoveSchedule(event_id=event_id, schedule_id=schedule_id)
        current_app.application.execute(cmd)
        return Response(status=204)
    except ValueError as e:
        return {"error": str(e)}, 400


@event_bp.route(
    "/events/<uuid:event_id>/schedule/<int:schedule_id>/results", methods=["POST"]
)
@api_auth.login_required
def upload_result(event_id, schedule_id):
    from utils.file_validation import validate_file, secure_filename

    uploaded_file = request.files.get("file")
    allowed_extensions = {"csv", "jpg", "jpeg", "png"}

    # Validate the file
    is_valid, error_message = validate_file(uploaded_file, allowed_extensions)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Generate a secure filename
    secure_name = secure_filename(uploaded_file.filename)

    cmd = UploadRaceResult(
        event_id=event_id,
        schedule_id=schedule_id,
        file=uploaded_file,
        filename=secure_name,
    )
    current_app.application.execute(cmd)
    return Response(status=204)


@event_bp.route("/events/<uuid:event_id>/result", methods=["POST"])
@api_auth.login_required
def add_race_result(event_id):
    cmd = AddEventResult(event_id=event_id, **request.json)
    current_app.application.execute(cmd)
    return Response(status=204)
