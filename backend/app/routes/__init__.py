from .dashboard import bp as dashboard_bp
from .messages import bp as messages_bp
from .progress import bp as progress_bp
from .quizzes import bp as quizzes_bp
from .tracks import bp as tracks_bp


def register_routes(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tracks_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(messages_bp)
