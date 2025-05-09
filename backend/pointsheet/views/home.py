from flask import Blueprint, render_template, current_app

from modules.event.queries.get_available_events import GetAvailableEvents
from modules.event.queries.get_ongoing_events import GetOngoingEvents
from pointsheet.auth import web_auth, get_user_id

home_bp = Blueprint("home", __name__, url_prefix="/home")


@home_bp.route("/", methods=["GET"])
@web_auth.login_required
def home():
    return render_template("home/index.html")


@home_bp.route("/race_cards", methods=["GET"])
@web_auth.login_required
def home_race_cards():
    user_id = get_user_id()

    # Get events the user is participating in
    ongoing_result = current_app.application.execute(GetOngoingEvents(user_id=user_id))
    ongoing_events = [evt.model_dump() for evt in ongoing_result]

    # Get available events and find the next one
    available_result = current_app.application.execute(
        GetAvailableEvents(user_id=user_id)
    )
    available_events = [evt.model_dump() for evt in available_result]

    # Sort available events by start date and get the next one
    next_event = None
    if available_events:
        sorted_events = sorted(available_events, key=lambda e: e.get("starts_at", ""))
        next_event = sorted_events[0] if sorted_events else None

    # For now, we don't have a proper implementation for getting the last race
    # This would require implementing the GetRecentEvent query
    last_race = None

    return render_template(
        "home/index.html",
        ongoing_events=ongoing_events,
        next_event=next_event,
        last_race=last_race,
    )


@home_bp.route("/available_events", methods=["GET"])
@web_auth.login_required
def available_events():
    result = current_app.application.execute(GetAvailableEvents(user_id=get_user_id()))
    events = [evt.model_dump() for evt in result]
    return render_template("home/list_events.html", events=events)


@home_bp.route("/ongoing-events", methods=["GET"])
@web_auth.login_required
def ongoing_events():
    result = current_app.application.execute(GetOngoingEvents(user_id=get_user_id()))
    events = [evt.model_dump() for evt in result]
    return render_template("home/list_events.html", events=events)
