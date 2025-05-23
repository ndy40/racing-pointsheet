from http import HTTPStatus

from flask import Blueprint, current_app, request, Response
from pointsheet.auth import api_auth, get_user_id

from modules.auth.commands.authenticate_user import AuthUser
from modules.auth.query.get_active_user import GetActiveUser
from modules.auth.commands.register_user import RegisterUser
from modules.auth.query.get_user_by_id import GetUserById
from modules.auth.responses import CurrentUserResponse

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    current_app.application.execute(RegisterUser(**request.json))
    return Response(status=HTTPStatus.NO_CONTENT)


@auth_bp.route("/auth", methods=["POST"])
def authenticate():
    cmd = AuthUser(**request.json)
    current_app.application.execute(cmd)
    active_user = current_app.application.execute(GetActiveUser(username=cmd.username))
    return {"token": active_user.auth_token}


@auth_bp.route("/auth", methods=["GET"])
@api_auth.login_required
def get_current_user():
    # Get the current user's ID using get_user_id()
    user_id = get_user_id()

    if not user_id:
        return {
            "error": "Unauthorized",
            "message": "Invalid or expired token.",
        }, HTTPStatus.UNAUTHORIZED

    # Get the user by ID
    active_user = current_app.application.execute(GetUserById(user_id=user_id))

    # Create a response using the pydantic model
    response = CurrentUserResponse(username=active_user.username, role=active_user.role)

    # Return the response as a dictionary
    return response.model_dump()
