from flask import Blueprint, request, current_app, Response

from api.utils import auth
from modules.event.commands.create_event import CreateEvent
from modules.event.queries.get_event import GetEvent
from pointsheet.domain.responses import ResourceCreated

event_bp = Blueprint("events", __name__)


@event_bp.route("/events/", methods=["POST"])
@auth.login_required
def events():
    cmd = CreateEvent(**request.json)
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=cmd.id))
    return ResourceCreated(resource=str(event.id)).model_dump(), 201


@event_bp.route("/events/<event_id>/", methods=["GET"])
def get_event(event_id):
    query = GetEvent(event_id=event_id)
    event = current_app.application.execute(query)
    return (event.model_dump(), 200) if event else Response(status=404)
