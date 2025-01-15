from flask import Blueprint, request, current_app

from modules.event.commands.create_event import CreateEvent
from modules.event.queries.get_event import GetEvent
from pointsheet.domain.responses import ResourceCreated

event_bp = Blueprint("events", __name__)


@event_bp.route("/events/", methods=["POST"])
def events():
    cmd = CreateEvent(**request.json)
    current_app.application.execute(cmd)
    event = GetEvent(event_id=cmd.id)
    return ResourceCreated(resource=event.id).model_dump(), 201
