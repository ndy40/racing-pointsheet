import json
import logging
import os
from pathlib import Path

from flask import Flask, render_template, Response, session, redirect
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from pydantic import ValidationError

import views
from api import api_bp

root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, "static")
template_directory = os.path.join(root_dir, "templates")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(
        __name__,
        static_folder=static_directory,
        template_folder=template_directory,
    )
    csrf.init_app(app)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "point_sheets.db.sqlite"),
        WTF_CSRF_CHECK_DEFAULT=False,
        WTF_CSRF_EXEMPT_ROUTES=["/api/*"],
        SQLALCHEMY_ECHO=True,
        DEBUG=True,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        if session.get("token"):
            return redirect("/home")
        return redirect("/auth")

    @app.route("/api")
    def api():
        return render_template("docs.html")

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

    @app.context_processor
    def inject_is_authenticated():
        return dict(
            is_authenticated=session.get("is_authenticated", False),
            user_id=session.get("user_id", None),
        )

    # @app.errorhandler(Exception)
    # def handle_all_exceptions(e: Exception):
    #     resp = {
    #         "code": HTTPStatus.INTERNAL_SERVER_ERROR,
    #         "message": str(e),
    #     }
    #     return Response(
    #         content_type="application/json",
    #         status=resp["code"],
    #         response=json.dumps(resp),
    #     )

    from modules import application

    app.application = application

    app.register_blueprint(api_bp)
    csrf.exempt(api_bp)
    app.register_blueprint(views.views_bp)

    return app
