from flask import Blueprint, current_app, Response, jsonify, request

from modules.event.queries.get_all_cars import GetAllCars
from pointsheet.auth import api_auth

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")


@cars_bp.route("/", methods=["GET"])
@api_auth.login_required
def get_cars():
    """
    Get all cars with optional filtering by game.
    
    Returns:
        A JSON array of all cars matching the filter criteria.
    """
    # Extract query parameters
    query_params = request.args.to_dict()
    
    # Create and execute the query
    query = GetAllCars(**query_params)
    cars = current_app.application.execute(query)
    
    # Return the results
    return [car.model_dump() for car in cars] if cars else []