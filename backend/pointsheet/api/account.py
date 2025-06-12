from http import HTTPStatus

from flask import Blueprint, current_app
from pointsheet.auth import api_auth

from modules.account.queries.get_all_drivers import GetAllDrivers
from modules.account.responses import DriverResponse, DriversResponse

account_bp = Blueprint("account", __name__)


@account_bp.route("/account/drivers", methods=["GET"])
@api_auth.login_required
def get_all_drivers():
    # Execute the query to get all drivers
    drivers = current_app.application.execute(GetAllDrivers())
    
    # Map the drivers to the response model
    return [
        DriverResponse(id=driver.id, name=driver.name, role=driver.role).model_dump()
        for driver in drivers
    ], HTTPStatus.OK
