from flask import Blueprint

from .events import event_bp, series_bp
from .auth import auth_bp

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(event_bp)
api_blueprint.register_blueprint(series_bp)
api_blueprint.register_blueprint(auth_bp)
