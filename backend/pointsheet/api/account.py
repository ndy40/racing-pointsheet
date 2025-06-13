from http import HTTPStatus

from flask import Blueprint, current_app, Response
from pointsheet.auth import api_auth

from modules.account.queries.get_all_drivers import GetAllDrivers
from modules.account.queries.get_user import GetUser
from modules.account.responses import DriverResponse, DriversResponse
from pointsheet.domain.types import EntityId

account_bp = Blueprint("account", __name__, url_prefix='accounts')


@account_bp.route("/drivers", methods=["GET"])
@api_auth.login_required
def get_all_drivers():
    # Execute the query to get all drivers
    drivers = current_app.application.execute(GetAllDrivers())

    # Map the drivers to the response model
    return [
        DriverResponse(id=driver.id, name=driver.name, role=driver.role).model_dump()
        for driver in drivers
    ], HTTPStatus.OK


@account_bp.route("/drivers/<uuid:id>", methods=["GET"])
@api_auth.login_required
def get_driver(id):
    # Execute the query to get a specific driver
    driver = current_app.application.execute(GetUser(user_id=id))

    if not driver:
        return Response(status=404)

    # Map the driver to the response model
    return DriverResponse(id=driver.id, name=driver.name, role=driver.role).model_dump(), HTTPStatus.OK
