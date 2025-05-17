from flask import Blueprint

from .auth import auth_bp
from .events import event_bp
from .events import series_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(event_bp)
api_bp.register_blueprint(series_bp)
