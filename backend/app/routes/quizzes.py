from flask import Blueprint, current_app, jsonify, request

from ..services import quiz_service
from ..utils.validation import require_json

bp = Blueprint("quizzes", __name__, url_prefix="/api")


@bp.get("/quizzes/<int:quiz_id>")
def get_quiz(quiz_id):
    quiz = quiz_service.get_quiz(quiz_id)
    return jsonify({"quiz": quiz})


@bp.post("/quizzes/<int:quiz_id>/submit")
def submit_quiz(quiz_id):
    user_id = current_app.config["DEFAULT_USER_ID"]
    payload = require_json(request)
    result = quiz_service.submit_quiz(quiz_id, user_id, payload)
    return jsonify({"result": result})
