import json
import os
from http import HTTPStatus
from pathlib import Path

from flask import Flask, render_template, Response

from pydantic import ValidationError

from api.auth import auth_bp
from api.events import series_bp, event_bp


root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, "static")
template_directory = os.path.join(root_dir, "templates")


def create_app(test_config=None):
    app = Flask(
        __name__,
        static_folder=static_directory,
        template_folder=template_directory,
    )

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "point_sheets.db.sqlite"),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

    from pointsheet.domain.exceptions.base import PointSheetException

    @app.errorhandler(PointSheetException)
    def app_error_handler(e):
        resp = {
            "code": e.code if hasattr(e, "code") else 400,
            "message": e.message if hasattr(e, "message") else str(e),
        }

        return Response(
            content_type="application/json",
            status=resp["code"],
            response=json.dumps(resp),
        )

    @app.errorhandler(ValidationError)
    def app_validation_error(e: ValidationError):
        resp = {
            "code": 400,
            "message": e.errors(
                include_input=False, include_url=False, include_context=False
            ),
        }
        return Response(
            content_type="application/json",
            status=resp["code"],
            response=json.dumps(resp),
        )

    @app.errorhandler(Exception)
    def handle_all_exceptions(e: Exception):
        resp = {
            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": str(e),
        }
        return Response(
            content_type="application/json",
            status=resp["code"],
            response=json.dumps(resp),
        )

    from modules import application

    app.application = application

    app.register_blueprint(series_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(auth_bp)

    return app
