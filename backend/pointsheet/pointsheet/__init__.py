import json
import os
from http import HTTPStatus
from pathlib import Path

from api.auth import auth_bp
from api.events import series_bp, event_bp
from celery import Celery, Task
from flask import Flask, render_template, Response
from pydantic import ValidationError


root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, "static")
template_directory = os.path.join(root_dir, "templates")


def celery_ini_app(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # Function to collect all submodules under 'modules'
    def _celery_collect_submodules(directory):
        submodules = []
        for root, dirs, files in os.walk(directory):
            if "__init__.py" in files:
                module_name = root.replace(os.path.sep, ".")
                submodules.append(module_name)
        return submodules

    celery_worker = Celery("pointsheet", task_cls=FlaskTask)
    celery_worker.config_from_object("pointsheet.celeryconfig")
    celery_worker.set_default()
    celery_worker.autodiscover_tasks(_celery_collect_submodules("modules"))
    app.extensions["celery"] = celery_worker
    return celery_worker


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

    celery_ini_app(app)

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
            "message": dict(
                list(
                    map(
                        lambda err: (err["loc"][0], err["msg"])
                        if err["loc"]
                        else ("message", err["msg"]),
                        e.errors(
                            include_input=False,
                            include_url=False,
                            include_context=False,
                        ),
                    )
                )
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
