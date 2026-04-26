from ..db import connection

def get_analytics():
    db = connection.get_db()
    # Total users
    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    # Total quiz attempts
    total_quiz_attempts = db.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0]
    # Average score
    avg_score = db.execute("SELECT AVG(score) FROM quiz_attempts").fetchone()[0] or 0
    # Number of completed topics
    completed_topics = db.execute("SELECT COUNT(*) FROM completed_topics").fetchone()[0]
    # Quiz attempts per track
    attempts_per_track = db.execute("""
        SELECT tracks.title, COUNT(quiz_attempts.id) as count
        FROM quiz_attempts
        JOIN quizzes ON quiz_attempts.quiz_id = quizzes.id
        JOIN modules ON quizzes.module_id = modules.id
        JOIN tracks ON modules.track_id = tracks.id
        GROUP BY tracks.title
    """).fetchall()

    return {
        "total_users": total_users,
        "total_quiz_attempts": total_quiz_attempts,
        "average_score": round(avg_score, 2),
        "completed_topics": completed_topics,
        "attempts_per_track": [{"track": row[0], "count": row[1]} for row in attempts_per_track]
    }