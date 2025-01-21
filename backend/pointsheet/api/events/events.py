from flask import Blueprint, request, current_app, Response

from modules.event.commands.create_event import CreateEvent
from modules.event.queries.get_event import GetEvent
from modules.event.queries.get_events import GetEvents
from pointsheet.auth import auth
from pointsheet.domain.responses import ResourceCreated

event_bp = Blueprint("events", __name__)


@event_bp.route("/events/", methods=["POST"])
@auth.login_required
def events():
    cmd = CreateEvent(**request.json)
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=cmd.id))
    return ResourceCreated(resource=str(event.id)).model_dump(), 201


@event_bp.route("/events/", methods=["GET"])
@auth.login_required
def get_events():
    cmd = GetEvents()
    all_events = current_app.application.execute(cmd)
    return [evt.model_dump() for evt in all_events] if events else []


@event_bp.route("/events/<uuid:event_id>/", methods=["GET"])
@auth.login_required
def get_event(event_id):
    query = GetEvent(event_id=event_id)
    event = current_app.application.execute(query)
    return (event.model_dump(), 200) if event else Response(status=404)
