import json
import logging
import os
from pathlib import Path

import sentry_sdk
from flask import Flask, render_template, Response, session, redirect, abort
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from pydantic import ValidationError

import views
from api import api_bp
from pointsheet.config import config as app_config

root_dir = os.path.join(Path(__file__).parent.parent)

static_directory = os.path.join(root_dir, "static")
template_directory = os.path.join(root_dir, "templates")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


sentry_sdk.init(
    dsn=app_config.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=False,
    environment=app_config.APP_ENV,
)

if not os.path.exists(app_config.UPLOAD_FOLDER):
    os.makedirs(app_config.UPLOAD_FOLDER)


def create_app(test_config=None):
    # Get environment from environment variable, default to development
    app = Flask(
        __name__,
        static_folder=static_directory,
        template_folder=template_directory,
    )
    # Load configuration from the appropriate config class
    app.config.from_object(app_config)

    csrf = CSRFProtect()
    csrf.init_app(app)
    CORS(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        if session.get("token"):
            return redirect("/home")
        return redirect("/auth")

    @app.route(
        "/api",
    )
    @csrf.exempt
    def api():
        return render_template("docs.html")

    @app.route("/uploads/<path:filename>")
    @csrf.exempt
    def serve_uploaded_file(filename):
        """
        Serve files from the upload folder.

        Args:
            filename: The name of the file to serve

        Returns:
            The file content with the appropriate MIME type
        """
        try:
            # Get the file content using the file_store
            file_content = app_config.file_store.fetch_file(filename)

            # Determine the MIME type based on the file extension
            extension = os.path.splitext(filename)[1].lower().lstrip(".")
            content_types = {
                "jpeg": "image/jpeg",
                "jpg": "image/jpeg",
                "png": "image/png",
                "csv": "text/csv",
                "pdf": "application/pdf",
            }
            content_type = content_types.get(extension, "application/octet-stream")

            # Create a response with the file content and MIME type
            return Response(file_content, mimetype=content_type)
        except FileNotFoundError:
            abort(404, description=f"File {filename} not found")
        except Exception as e:
            logger.exception(f"Error serving file {filename}: {str(e)}")
            abort(500, description=f"Error serving file: {str(e)}")

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
        """
        Handle Pydantic validation errors and return a standardized response.

        Args:
            e (ValidationError): The validation error raised by Pydantic

        Returns:
            Response: A standardized JSON response with validation error details
        """
        # Get simplified error details without extra context
        errors = e.errors(
            include_input=False,
            include_url=False,
            include_context=False,
        )

        # Transform errors into a more readable format
        error_dict = {}
        for err in errors:
            # Use the field name as the key if available, otherwise use "message"
            key = err["loc"][0] if err.get("loc") else "message"
            error_dict[key] = err["msg"]

        # Create the response object
        resp = {"code": 400, "message": "Validation error", "errors": error_dict}

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

    @app.errorhandler(Exception)
    def handle_all_exceptions(e: Exception):
        # Log the exception
        logger.exception(f"Unhandled exception: {str(e)}")

        # Import here to avoid circular imports
        from http import HTTPStatus

        # Create a standardized error response
        resp = {
            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": "An unexpected error occurred",
            "error_type": e.__class__.__name__,
        }

        # In development mode, include the actual error message
        if app.config.get("DEBUG", False):
            resp["debug_message"] = str(e)

        return Response(
            content_type="application/json",
            status=resp["code"],
            response=json.dumps(resp),
        )

    from modules import application

    app.application = application

    app.register_blueprint(api_bp)
    csrf.exempt(api_bp)
    app.register_blueprint(views.views_bp)

    return app
