import os
import sqlite3
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv("DATABASE_PATH", REPO_ROOT / "database" / "cyberlearn.db"))
SCHEMA_PATH = REPO_ROOT / "database" / "schema.sql"


def seed_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON;")
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema_sql)

        connection.executescript(
            """
            DELETE FROM message_analysis_history;
            DELETE FROM completed_topics;
            DELETE FROM user_progress;
            DELETE FROM quiz_attempts;
            DELETE FROM answer_options;
            DELETE FROM questions;
            DELETE FROM quizzes;
            DELETE FROM modules;
            DELETE FROM tracks;
            DELETE FROM users;
            """
        )

        connection.execute(
            "INSERT INTO users (id, name) VALUES (?, ?);",
            (1, "Default Learner"),
        )

        tracks = [
            (1, "Message and Email Defense", "Learn to detect phishing and social engineering patterns.", 1),
            (2, "Account and Device Security", "Protect credentials, devices, and accounts from compromise.", 2),
        ]
        connection.executemany(
            "INSERT INTO tracks (id, title, description, order_index) VALUES (?, ?, ?, ?);",
            tracks,
        )

        modules = [
            (1, 1, "Spot Phishing Red Flags", "Identify urgent language, spoofed domains, and unusual asks.", "phishing-red-flags", 1),
            (2, 1, "Safe Link Handling", "Inspect links and attachments before taking action.", "safe-link-handling", 2),
            (3, 2, "Strong Password Habits", "Build resilient password and passphrase routines.", "strong-password-habits", 1),
            (4, 2, "MFA and Recovery", "Use multi-factor authentication and secure recovery flows.", "mfa-and-recovery", 2),
        ]
        connection.executemany(
            """
            INSERT INTO modules (id, track_id, title, description, topic_key, order_index)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            modules,
        )

        quizzes = [
            (1, 1, "Phishing Basics Quiz", "Test your understanding of common phishing indicators."),
            (2, 2, "Link Safety Quiz", "Practice decisions for URLs and attachments."),
            (3, 3, "Password Security Quiz", "Assess your password hygiene and storage decisions."),
            (4, 4, "MFA Essentials Quiz", "Verify your understanding of MFA and account recovery."),
        ]
        connection.executemany(
            "INSERT INTO quizzes (id, module_id, title, description) VALUES (?, ?, ?, ?);",
            quizzes,
        )

        questions = [
            (1, 1, "Which sign is most likely phishing?", 1),
            (2, 1, "What should you do with an urgent payment email from a new sender?", 2),
            (3, 2, "Before clicking a shortened URL, you should:", 1),
            (4, 2, "An attachment from an unknown sender should be:", 2),
            (5, 3, "Which password is strongest?", 1),
            (6, 3, "Where is it safest to store passwords?", 2),
            (7, 4, "What is the main benefit of MFA?", 1),
            (8, 4, "Recovery codes should be:", 2),
        ]
        connection.executemany(
            "INSERT INTO questions (id, quiz_id, prompt, order_index) VALUES (?, ?, ?, ?);",
            questions,
        )

        options = [
            (1, 1, "A", "A message with perfect branding and expected context.", 0),
            (2, 1, "B", "An email demanding immediate gift card purchases.", 1),
            (3, 1, "C", "A calendar invite from your direct manager.", 0),
            (4, 1, "D", "A routine password reset request you initiated.", 0),
            (5, 2, "A", "Reply and ask for confirmation in the same email thread.", 0),
            (6, 2, "B", "Pay immediately to avoid delays.", 0),
            (7, 2, "C", "Verify through a trusted channel before acting.", 1),
            (8, 2, "D", "Forward to coworkers for a vote.", 0),
            (9, 3, "A", "Use a preview tool or hover to inspect destination.", 1),
            (10, 3, "B", "Click quickly before the offer expires.", 0),
            (11, 3, "C", "Disable browser protections and open it.", 0),
            (12, 3, "D", "Post it in a public chat for help.", 0),
            (13, 4, "A", "Opened only on a personal unmanaged device.", 0),
            (14, 4, "B", "Scanned and verified before opening.", 1),
            (15, 4, "C", "Uploaded to random converters online.", 0),
            (16, 4, "D", "Ignored if the filename looks normal.", 0),
            (17, 5, "A", "Summer2024", 0),
            (18, 5, "B", "P@ssword123!", 0),
            (19, 5, "C", "Blue!River!Orbit!Candle!73", 1),
            (20, 5, "D", "qwerty", 0),
            (21, 6, "A", "In an encrypted password manager.", 1),
            (22, 6, "B", "In plain text notes synced publicly.", 0),
            (23, 6, "C", "On a sticky note under the keyboard.", 0),
            (24, 6, "D", "Shared in team chat.", 0),
            (25, 7, "A", "It adds a second verification step.", 1),
            (26, 7, "B", "It removes the need for passwords forever.", 0),
            (27, 7, "C", "It encrypts every file on your device.", 0),
            (28, 7, "D", "It blocks all phishing automatically.", 0),
            (29, 8, "A", "Printed or stored securely offline.", 1),
            (30, 8, "B", "Posted on social media for backup.", 0),
            (31, 8, "C", "Saved in unencrypted shared drives.", 0),
            (32, 8, "D", "Ignored because they are optional.", 0),
        ]
        connection.executemany(
            """
            INSERT INTO answer_options (id, question_id, label, option_text, is_correct)
            VALUES (?, ?, ?, ?, ?);
            """,
            options,
        )

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
    print(f"Database seeded at {DB_PATH}")
