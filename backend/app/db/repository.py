import json
from datetime import date, datetime, timedelta

from .connection import get_db


def _rows_to_dicts(rows):
    return [dict(row) for row in rows]


def get_track(track_id):
    db = get_db()
    row = db.execute(
        "SELECT id, title, description FROM tracks WHERE id = ?;",
        (track_id,),
    ).fetchone()
    return dict(row) if row else None


def get_tracks_for_user(user_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT
            t.id,
            t.title,
            t.description,
            COUNT(m.id) AS moduleCount,
            SUM(CASE WHEN ct.module_id IS NOT NULL THEN 1 ELSE 0 END) AS completedModules
        FROM tracks t
        LEFT JOIN modules m ON m.track_id = t.id
        LEFT JOIN completed_topics ct ON ct.module_id = m.id AND ct.user_id = ?
        GROUP BY t.id
        ORDER BY t.order_index ASC, t.id ASC;
        """,
        (user_id,),
    ).fetchall()

    result = []
    for row in rows:
        item = dict(row)
        module_count = item["moduleCount"] or 0
        completed_modules = item["completedModules"] or 0
        completion = round((completed_modules / module_count) * 100, 2) if module_count else 0.0
        item["completionPercent"] = completion
        result.append(item)

    return result


def get_modules_for_track(track_id, user_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT
            m.id,
            m.track_id AS trackId,
            m.title,
            m.description,
            m.topic_key AS topicKey,
            m.order_index AS orderIndex,
            COALESCE(up.completion_percent, 0) AS completionPercent,
            up.last_score AS lastScore,
            CASE WHEN ct.module_id IS NULL THEN 0 ELSE 1 END AS completed,
            q.id AS quizId
        FROM modules m
        LEFT JOIN user_progress up ON up.module_id = m.id AND up.user_id = ?
        LEFT JOIN completed_topics ct ON ct.module_id = m.id AND ct.user_id = ?
        LEFT JOIN quizzes q ON q.module_id = m.id
        WHERE m.track_id = ?
        ORDER BY m.order_index ASC, m.id ASC;
        """,
        (user_id, user_id, track_id),
    ).fetchall()

    modules = []
    for row in rows:
        item = dict(row)
        item["completed"] = bool(item["completed"])
        modules.append(item)

    return modules


def get_quiz_with_questions(quiz_id):
    db = get_db()
    quiz_row = db.execute(
        """
        SELECT
            q.id,
            q.module_id AS moduleId,
            q.title,
            q.description,
            m.title AS moduleTitle
        FROM quizzes q
        JOIN modules m ON m.id = q.module_id
        WHERE q.id = ?;
        """,
        (quiz_id,),
    ).fetchone()

    if quiz_row is None:
        return None

    quiz = dict(quiz_row)

    question_rows = db.execute(
        """
        SELECT id, prompt, order_index AS orderIndex
        FROM questions
        WHERE quiz_id = ?
        ORDER BY order_index ASC, id ASC;
        """,
        (quiz_id,),
    ).fetchall()

    questions = []
    for question_row in question_rows:
        question = dict(question_row)
        option_rows = db.execute(
            """
            SELECT id, label, option_text AS text
            FROM answer_options
            WHERE question_id = ?
            ORDER BY id ASC;
            """,
            (question["id"],),
        ).fetchall()
        question["options"] = _rows_to_dicts(option_rows)
        questions.append(question)

    quiz["questions"] = questions
    return quiz


def get_correct_options_for_quiz(quiz_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT q.id AS questionId, ao.id AS optionId
        FROM questions q
        JOIN answer_options ao ON ao.question_id = q.id
        WHERE q.quiz_id = ? AND ao.is_correct = 1;
        """,
        (quiz_id,),
    ).fetchall()
    return {row["questionId"]: row["optionId"] for row in rows}


def create_quiz_attempt(user_id, quiz_id, score, total_questions, correct_answers):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO quiz_attempts (user_id, quiz_id, score, total_questions, correct_answers)
        VALUES (?, ?, ?, ?, ?);
        """,
        (user_id, quiz_id, score, total_questions, correct_answers),
    )
    db.commit()
    return cursor.lastrowid


def module_exists(module_id):
    db = get_db()
    row = db.execute("SELECT id FROM modules WHERE id = ?;", (module_id,)).fetchone()
    return row is not None


def upsert_progress(user_id, module_id, completion_percent, last_score=None):
    db = get_db()
    db.execute(
        """
        INSERT INTO user_progress (user_id, module_id, completion_percent, last_score)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, module_id)
        DO UPDATE SET
            completion_percent = MAX(user_progress.completion_percent, excluded.completion_percent),
            last_score = COALESCE(excluded.last_score, user_progress.last_score),
            updated_at = CURRENT_TIMESTAMP;
        """,
        (user_id, module_id, completion_percent, last_score),
    )
    db.commit()


def mark_topic_completed(user_id, module_id):
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO completed_topics (user_id, module_id) VALUES (?, ?);",
        (user_id, module_id),
    )
    db.commit()


def get_progress_for_user(user_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT
            m.id AS moduleId,
            m.track_id AS trackId,
            m.title,
            COALESCE(up.completion_percent, 0) AS completionPercent,
            up.last_score AS lastScore,
            up.updated_at AS lastUpdatedAt,
            CASE WHEN ct.module_id IS NULL THEN 0 ELSE 1 END AS completed
        FROM modules m
        LEFT JOIN user_progress up ON up.module_id = m.id AND up.user_id = ?
        LEFT JOIN completed_topics ct ON ct.module_id = m.id AND ct.user_id = ?
        ORDER BY m.track_id ASC, m.order_index ASC;
        """,
        (user_id, user_id),
    ).fetchall()

    progress = []
    for row in rows:
        item = dict(row)
        item["completed"] = bool(item["completed"])
        progress.append(item)

    total_modules = len(progress)
    completed_modules = sum(1 for item in progress if item["completed"])
    average_completion = (
        round(sum(item["completionPercent"] for item in progress) / total_modules, 2)
        if total_modules
        else 0.0
    )

    return {
        "summary": {
            "totalModules": total_modules,
            "completedModules": completed_modules,
            "averageCompletionPercent": average_completion,
        },
        "modules": progress,
    }


def get_module_progress(user_id, module_id):
    db = get_db()
    row = db.execute(
        """
        SELECT
            m.id AS moduleId,
            m.track_id AS trackId,
            m.title,
            COALESCE(up.completion_percent, 0) AS completionPercent,
            up.last_score AS lastScore,
            up.updated_at AS lastUpdatedAt,
            CASE WHEN ct.module_id IS NULL THEN 0 ELSE 1 END AS completed
        FROM modules m
        LEFT JOIN user_progress up ON up.module_id = m.id AND up.user_id = ?
        LEFT JOIN completed_topics ct ON ct.module_id = m.id AND ct.user_id = ?
        WHERE m.id = ?;
        """,
        (user_id, user_id, module_id),
    ).fetchone()

    if row is None:
        return None

    item = dict(row)
    item["completed"] = bool(item["completed"])
    return item


def get_recent_quiz_attempts(user_id, limit=5):
    db = get_db()
    rows = db.execute(
        """
        SELECT qa.id, qa.quiz_id AS quizId, q.title AS quizTitle, qa.score, qa.submitted_at AS submittedAt
        FROM quiz_attempts qa
        JOIN quizzes q ON q.id = qa.quiz_id
        WHERE qa.user_id = ?
        ORDER BY qa.submitted_at DESC, qa.id DESC
        LIMIT ?;
        """,
        (user_id, limit),
    ).fetchall()
    return _rows_to_dicts(rows)


def _calculate_streak(attempt_dates):
    if not attempt_dates:
        return 0

    parsed_dates = {datetime.strptime(value, "%Y-%m-%d").date() for value in attempt_dates}
    cursor = max(parsed_dates)
    streak = 0

    while cursor in parsed_dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def get_dashboard_metrics(user_id):
    db = get_db()

    total_tracks = db.execute("SELECT COUNT(*) AS count FROM tracks;").fetchone()["count"]
    total_modules = db.execute("SELECT COUNT(*) AS count FROM modules;").fetchone()["count"]
    completed_modules = db.execute(
        "SELECT COUNT(*) AS count FROM completed_topics WHERE user_id = ?;",
        (user_id,),
    ).fetchone()["count"]

    completed_tracks = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM (
            SELECT t.id
            FROM tracks t
            JOIN modules m ON m.track_id = t.id
            LEFT JOIN completed_topics ct ON ct.module_id = m.id AND ct.user_id = ?
            GROUP BY t.id
            HAVING COUNT(m.id) = SUM(CASE WHEN ct.module_id IS NOT NULL THEN 1 ELSE 0 END)
        ) grouped;
        """,
        (user_id,),
    ).fetchone()["count"]

    average_score = db.execute(
        "SELECT AVG(score) AS averageScore FROM quiz_attempts WHERE user_id = ?;",
        (user_id,),
    ).fetchone()["averageScore"]

    attempt_days = db.execute(
        """
        SELECT DISTINCT DATE(submitted_at) AS day
        FROM quiz_attempts
        WHERE user_id = ?
        ORDER BY day DESC;
        """,
        (user_id,),
    ).fetchall()

    streak_days = _calculate_streak([row["day"] for row in attempt_days])

    return {
        "metrics": {
            "totalTracks": total_tracks,
            "completedTracks": completed_tracks,
            "totalModules": total_modules,
            "completedModules": completed_modules,
            "averageQuizScore": round(average_score, 2) if average_score is not None else 0.0,
            "streakDays": streak_days,
        },
        "recentQuizAttempts": get_recent_quiz_attempts(user_id),
        "trackProgress": get_tracks_for_user(user_id),
    }


def create_message_analysis_history(user_id, message_text, analysis):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO message_analysis_history (
            user_id,
            message_text,
            verdict,
            risk_level,
            red_flags_json,
            explanation,
            tips_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (
            user_id,
            message_text,
            analysis["verdict"],
            analysis["riskLevel"],
            json.dumps(analysis["redFlags"]),
            analysis["explanation"],
            json.dumps(analysis["tips"]),
        ),
    )
    db.commit()
    return cursor.lastrowid


def get_message_analysis_history(user_id, limit=20):
    db = get_db()
    rows = db.execute(
        """
        SELECT
            id,
            message_text AS message,
            verdict,
            risk_level AS riskLevel,
            red_flags_json AS redFlags,
            explanation,
            tips_json AS tips,
            created_at AS createdAt
        FROM message_analysis_history
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?;
        """,
        (user_id, limit),
    ).fetchall()

    history = []
    for row in rows:
        item = dict(row)
        item["redFlags"] = json.loads(item["redFlags"])
        item["tips"] = json.loads(item["tips"])
        history.append(item)

    return history
