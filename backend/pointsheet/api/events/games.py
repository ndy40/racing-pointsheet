from flask import Blueprint, current_app, Response, jsonify, request

from modules.event.queries.get_games import GetGames
from modules.event.queries.get_game import GetGame
from modules.event.queries.get_cars import GetCars
from pointsheet.auth import api_auth

games_bp = Blueprint("games", __name__, url_prefix="/games")


@games_bp.route("", methods=["GET"])
@api_auth.login_required
def get_games():
    """
    Get all games.

    Returns:
        A JSON array of all games.
    """
    query = GetGames()
    games = current_app.application.execute(query)

    return [game.model_dump() for game in games] if games else []


@games_bp.route("/<int:game_id>", methods=["GET"])
@api_auth.login_required
def get_game(game_id):
    """
    Get a specific game by ID.

    Args:
        game_id: The ID of the game to retrieve.

    Returns:
        A JSON object with the game details, or a 404 response if not found.
    """
    query = GetGame(game_id=game_id)
    game = current_app.application.execute(query)

    return (game.model_dump(), 200) if game else Response(status=404)


@games_bp.route("/<int:game_id>/cars", methods=["GET"])
@api_auth.login_required
def get_game_cars(game_id):
    """
    Get all cars for a specific game with pagination.

    Args:
        game_id: The ID of the game to retrieve cars for.

    Query Parameters:
        page: The page number (default: 1)
        page_size: The number of items per page (default: 20)

    Returns:
        A JSON object containing the paginated list of cars and pagination metadata.
    """
    # Extract pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    query = GetCars(game_id=game_id, page=page, page_size=page_size)
    result = current_app.application.execute(query)

    # The result is now always a PaginatedResponse
    return result.model_dump()
