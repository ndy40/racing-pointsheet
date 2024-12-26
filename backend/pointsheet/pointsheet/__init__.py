import json
import os
from pathlib import Path

from flask import Flask, render_template, Response

from pydantic import ValidationError

from api.events import event_bp
from modules import application
from pointsheet.config import Config
from pointsheet.domain.exceptions import PointSheetException

root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, "static")
template_directory = os.path.join(root_dir, "templates")

config = Config()

__all__ = ["config", "create_app"]


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
    app.register_blueprint(event_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

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

    app.application = application

    return app
