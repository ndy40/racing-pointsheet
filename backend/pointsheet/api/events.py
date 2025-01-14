from flask import Blueprint

event_bp = Blueprint("events", __name__)


@event_bp.route("/events")
def events():
    return "Hello World!"
