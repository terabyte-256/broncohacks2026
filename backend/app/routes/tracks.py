from flask import Blueprint, current_app, jsonify

from ..services import track_service

bp = Blueprint("tracks", __name__, url_prefix="/api")


@bp.get("/tracks")
def get_tracks():
    user_id = current_app.config["DEFAULT_USER_ID"]
    tracks = track_service.get_tracks(user_id)
    return jsonify({"tracks": tracks})


@bp.get("/tracks/<int:track_id>/modules")
def get_track_modules(track_id):
    user_id = current_app.config["DEFAULT_USER_ID"]
    payload = track_service.get_track_modules(track_id, user_id)
    return jsonify(payload)
