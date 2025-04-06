from flask import Blueprint, current_app, render_template

from modules.event.commands.join_event import JoinEvent
from modules.event.commands.leave_event import LeaveEvent
from modules.event.queries.get_event import GetEvent
from pointsheet.auth import get_user_id, web_auth

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.route("/<uuid:event_id>/join", methods=["PUT"])
@web_auth.login_required
def join_event(event_id):
    cmd = JoinEvent(event_id=event_id, driver_id=get_user_id())
    current_app.application.execute(cmd)
    event = current_app.application.execute(GetEvent(event_id=event_id))
    print("Update event ", event.model_dump())
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
