from flask import Blueprint, current_app, Response, jsonify, request

from modules.event.queries.get_all_tracks import GetAllTracks
from modules.event.queries.get_track_by_id import GetTrackById
from pointsheet.auth import api_auth

tracks_bp = Blueprint("tracks", __name__, url_prefix="/tracks")


@tracks_bp.route("", methods=["GET"])
@api_auth.login_required
def get_tracks():
    """
    Get all tracks.
    
    Returns:
        A JSON array of all tracks.
    """
    query = GetAllTracks(**request.args.to_dict())
    tracks = current_app.application.execute(query)
    return [track.model_dump() for track in tracks] if tracks else []


@tracks_bp.route("/<int:track_id>", methods=["GET"])
@api_auth.login_required
def get_track(track_id):
    """
    Get a track by ID.
    
    Args:
        track_id: The ID of the track to retrieve.
        
    Returns:
        A JSON object representing the track if found, 404 otherwise.
    """
    query = GetTrackById(track_id=track_id)
    track = current_app.application.execute(query)
    return (track.model_dump(), 200) if track else Response(status=404)