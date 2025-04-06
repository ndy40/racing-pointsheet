from flask import Blueprint

from .auth import auth_bp
from .home import home_bp
from .events import events_bp

views_bp = Blueprint("views", __name__)

views_bp.register_blueprint(auth_bp)
views_bp.register_blueprint(home_bp)
views_bp.register_blueprint(events_bp)


@views_bp.app_template_filter("datetime")
def format_datetime(value, format="%Y-%m-%d %H:%M %Z"):
    if value is None:
        return ""
    offset = value.strftime("%Z")

    if offset:
        # Format offset with colon (e.g., +00:00)
        offset = f"{offset[:3]}:{offset[3:]}"
        # Create GMT string
        gmt = f" GMT{offset}"
    else:
        gmt = ""

    return value.strftime(format) + gmt
