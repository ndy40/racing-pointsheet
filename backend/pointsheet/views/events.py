from flask import Blueprint, current_app, render_template, request

from modules.event.commands.create_event import CreateEvent
from modules.event.commands.join_event import JoinEvent
from modules.event.commands.leave_event import LeaveEvent
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


@events_bp.route("/<uuid:event_id>/", methods=["GET", "POST"])
@web_auth.login_required
def view_event(event_id):
    if request.method == "GET":
        event = current_app.application.execute(GetEvent(event_id=event_id))
        return render_template("events/edit.html", event=event.model_dump())
