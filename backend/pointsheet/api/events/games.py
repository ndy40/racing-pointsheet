from flask import Blueprint, current_app, Response, jsonify

from modules.event.queries.get_games import GetGames
from modules.event.queries.get_game import GetGame
from modules.event.queries.get_cars import GetCars
from pointsheet.auth import api_auth

games_bp = Blueprint("games", __name__, url_prefix="/games")


@games_bp.route("/", methods=["GET"])
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
    Get all cars for a specific game.
    
    Args:
        game_id: The ID of the game to retrieve cars for.
        
    Returns:
        A JSON array of all cars for the specified game.
    """
    query = GetCars(game_id=game_id)
    cars = current_app.application.execute(query)
    
    return [car.model_dump() for car in cars] if cars else []