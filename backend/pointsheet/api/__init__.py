from flask import Blueprint

from .auth import auth_bp
from .account import account_bp
from .events import event_bp
from .events import series_bp
from .events import tracks_bp
from .events import cars_bp
from .events import games_bp
from .webhooks import webhook_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(account_bp)
api_bp.register_blueprint(event_bp)
api_bp.register_blueprint(series_bp)
api_bp.register_blueprint(tracks_bp)
api_bp.register_blueprint(cars_bp)
api_bp.register_blueprint(games_bp)
api_bp.register_blueprint(webhook_bp)
