from flask import Blueprint, current_app

from modules.event.domain.queries import GetAllSeries

event_bp = Blueprint("event", __name__)


@event_bp.route("/events", methods=["GET"])
def fetch_series():
    current_app.application.execute(GetAllSeries())
    return {"status": True}
