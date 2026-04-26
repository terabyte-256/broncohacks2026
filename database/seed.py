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
            (1, "Beginner Track", "Learn the basics and spot everyday online threats through quick quizzes.", 1),
            (2, "Developer Track", "Explore real-world attack techniques and learn how to build secure code.", 2),
        ]
        connection.executemany(
            "INSERT INTO tracks (id, title, description, order_index) VALUES (?, ?, ?, ?);",
            tracks,
        )

        # ── Beginner Track: 4 modules ──────────────────────────────────────────
        modules = [
            (1, 1, "Phishing",           "Recognize fake emails and messages designed to steal your credentials.", "phishing",           1),
            (2, 1, "Social Engineering", "Spot psychological manipulation tactics used to trick people.",           "social-engineering", 2),
            (3, 1, "Auth & Passwords",   "Build strong password habits and use multi-factor authentication.",       "auth-passwords",     3),
            (4, 1, "Sessions",           "Understand session tokens and how attackers can hijack them.",            "sessions",           4),
        ]
        connection.executemany(
            "INSERT INTO modules (id, track_id, title, description, topic_key, order_index) VALUES (?, ?, ?, ?, ?, ?);",
            modules,
        )

        quizzes = [
            (1, 1, "Phishing Quiz",          "Test your ability to spot phishing indicators."),
            (2, 2, "Social Engineering Quiz", "Identify manipulation tactics and safe responses."),
            (3, 3, "Auth & Passwords Quiz",   "Assess your password hygiene and MFA knowledge."),
            (4, 4, "Sessions Quiz",           "Check your understanding of session security."),
        ]
        connection.executemany(
            "INSERT INTO quizzes (id, module_id, title, description) VALUES (?, ?, ?, ?);",
            quizzes,
        )

        # quiz_id, prompt, order_index
        questions = [
            # Phishing (quiz 1)
            (1,  1, "Which of these is the strongest sign of a phishing email?",                              1),
            (2,  1, "An email from 'support@paypa1.com' asks you to verify your account. What do you do?",   2),
            (3,  1, "What is 'spear phishing'?",                                                              3),
            (4,  1, "You get: 'You won $1,000! Click now — offer expires in 1 hour!' This is most likely:",  4),
            # Social Engineering (quiz 2)
            (5,  2, "What is the primary goal of a social engineering attack?",                               1),
            (6,  2, "Someone calls claiming to be IT support and asks for your password. You should:",        2),
            (7,  2, "What is 'pretexting'?",                                                                  3),
            (8,  2, "Which behavior is a classic social engineering red flag?",                               4),
            # Auth & Passwords (quiz 3)
            (9,  3, "Which password is the strongest?",                                                       1),
            (10, 3, "What is the safest way to store your passwords?",                                        2),
            (11, 3, "What is the main benefit of multi-factor authentication (MFA)?",                         3),
            (12, 3, "A site you use just had a data breach. What should you do first?",                       4),
            # Sessions (quiz 4)
            (13, 4, "What is a session cookie?",                                                              1),
            (14, 4, "You finish using a public library computer to check email. You should:",                 2),
            (15, 4, "Session hijacking happens when:",                                                        3),
            (16, 4, "Which practice best protects your active sessions?",                                     4),
        ]
        connection.executemany(
            "INSERT INTO questions (id, quiz_id, prompt, order_index) VALUES (?, ?, ?, ?);",
            questions,
        )

        # question_id, label, option_text, is_correct
        options = [
            # Q1
            (1,  1, "A", "An email with a professional company logo and expected context.",              0),
            (2,  1, "B", "An email demanding you click a link immediately or your account gets deleted.", 1),
            (3,  1, "C", "A newsletter from a site you subscribed to last week.",                        0),
            (4,  1, "D", "A password-reset email you yourself requested.",                               0),
            # Q2
            (5,  2, "A", "Click the link and log in to resolve the issue quickly.",                      0),
            (6,  2, "B", "Reply with your account details to prove your identity.",                      0),
            (7,  2, "C", "Navigate directly to paypal.com by typing it in your browser.",               1),
            (8,  2, "D", "Forward the email to friends as a warning.",                                   0),
            # Q3
            (9,  3, "A", "A phishing attack sent by physical mail.",                                     0),
            (10, 3, "B", "A targeted attack that uses personal info about you to seem believable.",     1),
            (11, 3, "C", "An attack that targets only email servers.",                                   0),
            (12, 3, "D", "Phishing conducted exclusively through phone calls.",                          0),
            # Q4
            (13, 4, "A", "A legitimate prize from a company you recently purchased from.",               0),
            (14, 4, "B", "A phishing attempt using urgency and reward bait to rush you into clicking.", 1),
            (15, 4, "C", "An official government tax rebate notification.",                              0),
            (16, 4, "D", "A security test sent by your IT department.",                                  0),
            # Q5
            (17, 5, "A", "Breaking through firewalls using exploit code.",                               0),
            (18, 5, "B", "Manipulating people into revealing sensitive info or taking unsafe actions.", 1),
            (19, 5, "C", "Installing viruses on public computers.",                                      0),
            (20, 5, "D", "Overloading websites with traffic.",                                           0),
            # Q6
            (21, 6, "A", "Provide the password since the issue sounds urgent.",                          0),
            (22, 6, "B", "Ask them to send an email instead and share it there.",                        0),
            (23, 6, "C", "Refuse and verify their identity through official channels.",                 1),
            (24, 6, "D", "Give them only the first half of your password.",                              0),
            # Q7
            (25, 7, "A", "Sending emails with misleading subject lines.",                                0),
            (26, 7, "B", "Creating a fabricated scenario to gain trust and extract information.",       1),
            (27, 7, "C", "Using fake pop-up windows to steal credentials.",                              0),
            (28, 7, "D", "Hiding malware inside image files.",                                           0),
            # Q8
            (29, 8, "A", "A vendor confirming your delivery address.",                                   0),
            (30, 8, "B", "A colleague sharing a project status update.",                                 0),
            (31, 8, "C", "Someone creating extreme urgency and demanding you keep it secret.",          1),
            (32, 8, "D", "HR sending a benefits enrollment reminder.",                                   0),
            # Q9
            (33, 9,  "A", "Summer2024",                                                                  0),
            (34, 9,  "B", "P@ssword123!",                                                                0),
            (35, 9,  "C", "Blue!River!Orbit!Candle!73",                                                  1),
            (36, 9,  "D", "qwerty456",                                                                   0),
            # Q10
            (37, 10, "A", "Write them in a notebook kept at your desk.",                                 0),
            (38, 10, "B", "Use one memorable password across all sites.",                                0),
            (39, 10, "C", "Store them in an encrypted password manager.",                               1),
            (40, 10, "D", "Save them in a browser with no master password set.",                         0),
            # Q11
            (41, 11, "A", "It automatically makes your passwords longer.",                              0),
            (42, 11, "B", "It adds a second verification step so stolen passwords alone are not enough.", 1),
            (43, 11, "C", "It encrypts all the files on your device.",                                  0),
            (44, 11, "D", "It blocks all phishing emails at the server level.",                         0),
            # Q12
            (45, 12, "A", "Wait to see if you start receiving spam.",                                    0),
            (46, 12, "B", "Change your password on that site immediately, and on any other site where you reused it.", 1),
            (47, 12, "C", "Delete the account and never use that site again.",                           0),
            (48, 12, "D", "Contact the site's CEO on LinkedIn.",                                         0),
            # Q13
            (49, 13, "A", "A file that stores your full browsing history.",                              0),
            (50, 13, "B", "A token the server gives you after login to identify your active session.",  1),
            (51, 13, "C", "An encrypted copy of your password stored on your device.",                   0),
            (52, 13, "D", "A tracking pixel embedded in marketing emails.",                              0),
            # Q14
            (53, 14, "A", "Just close the browser tab.",                                                 0),
            (54, 14, "B", "Click 'Log out' on the site, then close the browser.",                      1),
            (55, 14, "C", "Turn off the monitor.",                                                       0),
            (56, 14, "D", "Clear only the download history.",                                            0),
            # Q15
            (57, 15, "A", "Someone correctly guesses your password.",                                    0),
            (58, 15, "B", "An attacker steals your session token and accesses your account without your password.", 1),
            (59, 15, "C", "You accidentally stay logged in on your own device.",                         0),
            (60, 15, "D", "The server crashes and logs everyone out.",                                   0),
            # Q16
            (61, 16, "A", "Stay logged in on all devices permanently for convenience.",                  0),
            (62, 16, "B", "Use public Wi-Fi for all banking and shopping activities.",                   0),
            (63, 16, "C", "Use HTTPS websites and log out when done on shared or public devices.",      1),
            (64, 16, "D", "Disable all browser cookies so sessions can't be tracked.",                  0),
        ]
        connection.executemany(
            "INSERT INTO answer_options (id, question_id, label, option_text, is_correct) VALUES (?, ?, ?, ?, ?);",
            options,
        )

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
    print(f"Database seeded at {DB_PATH}")
