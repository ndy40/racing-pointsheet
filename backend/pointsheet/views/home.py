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
def home_race_cards():
    # query for user's last race and result.
    # Query for all events the user is participating in
    # Query for Next Event.
    ...


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
    print(events)
    return render_template("home/list_events.html", events=events)
