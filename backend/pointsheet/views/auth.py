from flask import (
    Blueprint,
    request,
    current_app,
    flash,
    redirect,
    session,
    render_template,
)

from modules.auth.commands.authenticate_user import AuthUser
from modules.auth.query.get_active_user import GetActiveUser
from pointsheet.domain.exceptions.base import PointSheetException

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth", methods=["POST", "GET"])
def authenticate():
    if request.method == "POST":
        try:
            print(request.form)
            cmd = AuthUser(**request.form)
            current_app.application.execute(cmd)
            active_user = current_app.application.execute(
                GetActiveUser(username=cmd.username)
            )
            session.clear()
            session["user_id"] = active_user.id
            session["is_authenticated"] = True
            session["token"] = active_user.auth_token

            return redirect("/")
        except PointSheetException as e:
            flash(e)

    return render_template("auth/login.html")
