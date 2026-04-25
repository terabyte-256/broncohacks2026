from flask import Blueprint, current_app, jsonify

from ..services import dashboard_service

bp = Blueprint("dashboard", __name__, url_prefix="/api")


@bp.get("/dashboard")
def get_dashboard():
    user_id = current_app.config["DEFAULT_USER_ID"]
    data = dashboard_service.get_dashboard(user_id)
    return jsonify(data)
