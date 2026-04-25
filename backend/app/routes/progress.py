from flask import Blueprint, current_app, jsonify, request

from ..services import progress_service
from ..utils.validation import require_json

bp = Blueprint("progress", __name__, url_prefix="/api")


@bp.get("/progress")
def get_progress():
    user_id = current_app.config["DEFAULT_USER_ID"]
    progress = progress_service.get_progress(user_id)
    return jsonify(progress)


@bp.post("/progress")
def update_progress():
    user_id = current_app.config["DEFAULT_USER_ID"]
    payload = require_json(request)
    updated = progress_service.update_progress(user_id, payload)
    return jsonify(updated)
