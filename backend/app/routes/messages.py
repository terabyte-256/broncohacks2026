from flask import Blueprint, current_app, jsonify, request

from ..services import message_service
from ..utils.validation import parse_int, parse_non_empty_string, require_json

bp = Blueprint("messages", __name__, url_prefix="/api")


@bp.post("/analyze-message")
def analyze_message():
    user_id = current_app.config["DEFAULT_USER_ID"]
    payload = require_json(request)
    message_text = parse_non_empty_string(payload.get("message"), "message", max_length=5000)
    analysis = message_service.analyze_and_store_message(user_id, message_text)
    return jsonify(analysis)


@bp.get("/message-history")
def message_history():
    user_id = current_app.config["DEFAULT_USER_ID"]
    limit = parse_int(request.args.get("limit", 20), "limit", minimum=1, maximum=100)
    history = message_service.get_message_history(user_id, limit)
    return jsonify({"history": history})
