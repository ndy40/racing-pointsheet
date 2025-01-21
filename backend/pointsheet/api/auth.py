from http import HTTPStatus

from flask import Blueprint, current_app, request, Response

from modules.auth.commands.authenticate_user import AuthUser
from modules.auth.query.get_active_user import GetActiveUser
from modules.auth.commands.register_user import RegisterUser

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
    print("Active user:", active_user.auth_token)
    return {"token": active_user.auth_token}
