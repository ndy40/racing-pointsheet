from flask import Blueprint, current_app, render_template, request, redirect

from modules.event.commands.add_event_schedule import AddEventSchedule
from modules.event.commands.create_event import CreateEvent
from modules.event.commands.join_event import JoinEvent
from modules.event.commands.leave_event import LeaveEvent
from modules.event.commands.remove_schedule import RemoveSchedule
from modules.event.commands.update_event import UpdateEventModel
from modules.event.queries.get_all_tracks import GetAllTracks
from modules.event.queries.get_event import GetEvent
from modules.event.queries.get_events import GetEvents
from pointsheet.auth import get_user_id, web_auth

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.route("/", methods=["GET"])
def index():
    cmd = GetEvents()
    events = current_app.application.execute(cmd)
    context = [event.dict() for event in events]
    return render_template("events/index.html", events=context)


@events_bp.route("/<uuid:event_id>/join", methods=["PUT"])
@web_auth.login_required
def join_event(event_id):
    cmd = JoinEvent(event_id=event_id, driver_id=get_user_id())
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=event_id))
    return render_template(
        "_partials/components/event_card.html", event=event.model_dump()
    )


@events_bp.route("/<uuid:event_id>/leave", methods=["PUT"])
@web_auth.login_required
def leave_event(event_id):
    cmd = LeaveEvent(event_id=event_id, driver_id=get_user_id())
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=event_id))
    return render_template(
        "_partials/components/event_card.html", event=event.model_dump()
    )


@events_bp.route("/create", methods=["GET", "POST"])
@web_auth.login_required
def create_event():
    if request.method == "GET":
        return render_template("events/create.html")

    app = current_app.application

    cmd = CreateEvent(**request.form.to_dict())
    app.execute(cmd)

    event = app.execute(GetEvent(event_id=cmd.id))

    headers = {"HX-Redirect": "/events/%s" % event.id}

    return (
        "created",
        201,
        headers,
    )


@events_bp.route("/<uuid:event_id>/", methods=["GET", "POST", "PATCH"])
@web_auth.login_required
def view_event(event_id):
    if request.method == "GET":
        event = current_app.application.execute(GetEvent(event_id=event_id))
        tracks = current_app.application.execute(GetAllTracks())
        tracks = [track.model_dump() for track in tracks]
        return render_template(
            "events/edit.html", event=event.model_dump(), tracks=tracks
        )
    elif request.method == "PATCH":
        cmd = UpdateEventModel(event_id=event_id, **request.form.to_dict())
        current_app.application.execute(cmd)
        headers = {"HX-Redirect": "/events/%s" % event_id}
        return "updated", 200, headers
    return None


@events_bp.route("/<uuid:event_id>/schedules", methods=["POST"])
@web_auth.login_required
def add_event_schedule(event_id):
    cmd = AddEventSchedule(event_id=event_id, **request.form.to_dict())
    current_app.application.execute(cmd)
    return redirect("/events/%s/schedules" % event_id)


@events_bp.route("/<uuid:event_id>/schedules", methods=["GET"])
@web_auth.login_required
def get_event_schedules(event_id):
    cmd = GetEvent(event_id=event_id)
    event = current_app.application.execute(cmd)
    return render_template(
        "_partials/components/schedule_table.html", event=event.model_dump()
    )


@events_bp.route("/<uuid:event_id>/schedules/<schedule_id>", methods=["DELETE"])
@web_auth.login_required
def remove_schedule(event_id, schedule_id: int):
    cmd = RemoveSchedule(event_id=event_id, schedule_id=schedule_id)
    current_app.application.execute(cmd)

    cmd = GetEvent(event_id=event_id)
    event = current_app.application.execute(cmd)
    return render_template(
        "_partials/components/schedule_table.html", event=event.model_dump()
    )
