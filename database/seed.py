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
            (3, "Developer Track", "Learn common web vulnerabilities like XSS, SQL Injection, and CSRF.", 3),
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
            (5, 3, "Cross-Site Scripting", "Understand how XSS attacks work and how to prevent them.", "xss", 1),
            (6, 3, "SQL Injection", "Learn how attackers exploit unsanitized database queries.", "sql-injection", 2),
            (7, 3, "Cross-Site Request Forgery", "Detect and defend against forged cross-origin requests.", "csrf", 3),
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
            (5, 5, "XSS Fundamentals Quiz", "Test your knowledge of cross-site scripting vulnerabilities."),
            (6, 6, "SQL Injection Quiz", "Assess your understanding of SQL injection risks and defenses."),
            (7, 7, "CSRF Defense Quiz", "Verify your grasp of cross-site request forgery protections."),
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
            # XSS
            (9,  5, "Which of the following is the most effective defense against stored XSS?", 1),
            (10, 5, "An attacker injects <script>document.cookie</script> into a comment field. What is the likely goal?", 2),
            # SQL Injection
            (11, 6, "Which coding practice best prevents SQL injection?", 1),
            (12, 6, "A login form accepts ' OR '1'='1 as a password and grants access. What is the root cause?", 2),
            # CSRF
            (13, 7, "What is the primary purpose of a CSRF token?", 1),
            (14, 7, "Which HTTP request type is most commonly exploited in CSRF attacks?", 2),
        ]
        connection.executemany(
            "INSERT INTO questions (id, quiz_id, prompt, order_index) VALUES (?, ?, ?, ?);",
            questions,
        )

        options = [
            (1,  1,  "A", "A message with perfect branding and expected context.", 0),
            (2,  1,  "B", "An email demanding immediate gift card purchases.", 1),
            (3,  1,  "C", "A calendar invite from your direct manager.", 0),
            (4,  1,  "D", "A routine password reset request you initiated.", 0),
            (5,  2,  "A", "Reply and ask for confirmation in the same email thread.", 0),
            (6,  2,  "B", "Pay immediately to avoid delays.", 0),
            (7,  2,  "C", "Verify through a trusted channel before acting.", 1),
            (8,  2,  "D", "Forward to coworkers for a vote.", 0),
            (9,  3,  "A", "Use a preview tool or hover to inspect destination.", 1),
            (10, 3,  "B", "Click quickly before the offer expires.", 0),
            (11, 3,  "C", "Disable browser protections and open it.", 0),
            (12, 3,  "D", "Post it in a public chat for help.", 0),
            (13, 4,  "A", "Opened only on a personal unmanaged device.", 0),
            (14, 4,  "B", "Scanned and verified before opening.", 1),
            (15, 4,  "C", "Uploaded to random converters online.", 0),
            (16, 4,  "D", "Ignored if the filename looks normal.", 0),
            (17, 5,  "A", "Summer2024", 0),
            (18, 5,  "B", "P@ssword123!", 0),
            (19, 5,  "C", "Blue!River!Orbit!Candle!73", 1),
            (20, 5,  "D", "qwerty", 0),
            (21, 6,  "A", "In an encrypted password manager.", 1),
            (22, 6,  "B", "In plain text notes synced publicly.", 0),
            (23, 6,  "C", "On a sticky note under the keyboard.", 0),
            (24, 6,  "D", "Shared in team chat.", 0),
            (25, 7,  "A", "It adds a second verification step.", 1),
            (26, 7,  "B", "It removes the need for passwords forever.", 0),
            (27, 7,  "C", "It encrypts every file on your device.", 0),
            (28, 7,  "D", "It blocks all phishing automatically.", 0),
            (29, 8,  "A", "Printed or stored securely offline.", 1),
            (30, 8,  "B", "Posted on social media for backup.", 0),
            (31, 8,  "C", "Saved in unencrypted shared drives.", 0),
            (32, 8,  "D", "Ignored because they are optional.", 0),
            # XSS – question 9
            (33, 9,  "A", "Escaping and encoding all user-supplied output.", 1),
            (34, 9,  "B", "Blocking all JavaScript on the server.", 0),
            (35, 9,  "C", "Using HTTPS instead of HTTP.", 0),
            (36, 9,  "D", "Storing user input in a database without modification.", 0),
            # XSS – question 10
            (37, 10, "A", "Crashing the web server.", 0),
            (38, 10, "B", "Stealing session cookies from other users.", 1),
            (39, 10, "C", "Encrypting the page content.", 0),
            (40, 10, "D", "Redirecting users to the homepage.", 0),
            # SQL Injection – question 11
            (41, 11, "A", "Using parameterized queries or prepared statements.", 1),
            (42, 11, "B", "Hashing all database column names.", 0),
            (43, 11, "C", "Storing queries in environment variables.", 0),
            (44, 11, "D", "Increasing the database connection timeout.", 0),
            # SQL Injection – question 12
            (45, 12, "A", "The server uses an outdated database engine.", 0),
            (46, 12, "B", "The application concatenates user input directly into a SQL query.", 1),
            (47, 12, "C", "The login page is served over HTTP.", 0),
            (48, 12, "D", "The password field has no character limit.", 0),
            # CSRF – question 13
            (49, 13, "A", "To ensure each form submission originates from the legitimate site.", 1),
            (50, 13, "B", "To encrypt the user's session cookie.", 0),
            (51, 13, "C", "To validate the user's password on every request.", 0),
            (52, 13, "D", "To prevent SQL injection in form fields.", 0),
            # CSRF – question 14
            (53, 14, "A", "GET requests, because they are always visible in the URL.", 0),
            (54, 14, "B", "State-changing requests such as POST, PUT, or DELETE.", 1),
            (55, 14, "C", "OPTIONS requests used in CORS preflight.", 0),
            (56, 14, "D", "HEAD requests, because they carry no body.", 0),
        ]
        connection.executemany(
            """
            INSERT INTO answer_options (id, question_id, label, option_text, is_correct)
            VALUES (?, ?, ?, ?, ?);
            """,
            options,
        )
        new_questions = [
            # XSS – quiz_id 5 (order_index continues from 2)
            (15, 5, "Which HTML attribute is most commonly abused to execute inline XSS payloads?", 3),
            (16, 5, "A developer writes: element.innerHTML = userInput; What is wrong with this?", 4),
            (17, 5, "What does a DOM-based XSS attack manipulate that stored/reflected XSS does not?", 5),
            (18, 5, "A page renders: <img src=\"x\" onerror=\"stealCookies()\"> from user input. What type of XSS is this if the payload is saved in the database?", 6),
            (19, 5, "Which output context requires JavaScript-specific escaping rather than just HTML escaping?", 7),
            (20, 5, "A Content Security Policy header is set to: default-src 'self'. What does this prevent?", 8),
            (21, 5, "Which property should replace innerHTML when inserting plain text content safely?", 9),
            # SQL Injection – quiz_id 6 (order_index continues from 2)
            (22, 6, "Given this query:\nSELECT * FROM users WHERE username = 'INPUT';\n\nUser enters: ' OR '1'='1' --\n\nWhat is the effect?", 3),
            (23, 6, "Which of the following parameterized query examples correctly prevents SQL injection in Python?", 4),
            (24, 6, "An attacker enters: 1; DROP TABLE orders; --\ninto an order ID field. What class of SQL injection is this?", 5),
            (25, 6, "A login form is protected by input length limits on the frontend only. Why is this insufficient?", 6),
            (26, 6, "Which SQL injection technique is used when the application returns no visible output but responds differently based on true/false conditions?", 7),
            (27, 6, "Given:\nSELECT * FROM products WHERE id = INPUT;\n\nAttacker enters: 1 UNION SELECT username, password, null, null FROM users --\n\nWhat is the attacker attempting?", 8),
            (28, 6, "What is the safest way to handle a dynamic column name when parameterized queries cannot be used for that value?", 9),
            # CSRF – quiz_id 7 (order_index continues from 2)
            (29, 7, "A CSRF token is effective because it is:", 3),
            (30, 7, "An attacker hosts a page with:\n<img src=\"https://bank.com/transfer?to=attacker&amount=1000\">\nWhy does this work as a CSRF attack?", 4),
            (31, 7, "Which cookie attribute prevents it from being sent on cross-origin requests triggered by third-party pages?", 5),
            (32, 7, "A developer says 'We use POST for all state changes so we are safe from CSRF.' Why is this incorrect?", 6),
            (33, 7, "What is the Double Submit Cookie pattern used for in CSRF defense?", 7),
            (34, 7, "An API accepts only JSON and requires the Content-Type: application/json header. Does this fully protect against CSRF?", 8),
            (35, 7, "Which of the following request origins would a correctly configured SameSite=Strict cookie be sent with?", 9),
        ]
        connection.executemany(
            "INSERT INTO questions (id, quiz_id, prompt, order_index) VALUES (?, ?, ?, ?);",
            new_questions,
        )

        new_options = [
            # Q15 – abused HTML attribute
            (57,  15, "A", "onerror, onclick, and other event handler attributes.", 1),
            (58,  15, "B", "The href attribute on anchor tags only.", 0),
            (59,  15, "C", "The class attribute on div elements.", 0),
            (60,  15, "D", "The alt attribute on image elements.", 0),
            # Q16 – innerHTML danger
            (61,  16, "A", "innerHTML only works with div elements and throws errors elsewhere.", 0),
            (62,  16, "B", "It parses and renders HTML including script tags and event handlers from userInput.", 1),
            (63,  16, "C", "innerHTML is deprecated and should be replaced with outerHTML.", 0),
            (64,  16, "D", "It converts special characters to Unicode automatically, preventing injection.", 0),
            # Q17 – DOM-based XSS
            (65,  17, "A", "The server database, persisting the payload for all future visitors.", 0),
            (66,  17, "B", "The HTTP response body returned directly by the server.", 0),
            (67,  17, "C", "The client-side DOM directly, using sources like location.hash or document.referrer.", 1),
            (68,  17, "D", "The browser cache, replaying payloads on repeat visits.", 0),
            # Q18 – stored XSS via onerror
            (69,  18, "A", "Reflected XSS, because the payload came from a URL parameter.", 0),
            (70,  18, "B", "Stored XSS, because the payload is persisted in the database and served to other users.", 1),
            (71,  18, "C", "DOM-based XSS, because it manipulates an HTML element attribute.", 0),
            (72,  18, "D", "Self XSS, because only the attacker who entered it is affected.", 0),
            # Q19 – JS string context escaping
            (73,  19, "A", "Inside an HTML <p> tag body.", 0),
            (74,  19, "B", "Inside a JavaScript string variable: var name = 'USER_INPUT';", 1),
            (75,  19, "C", "Inside an HTML title element.", 0),
            (76,  19, "D", "Inside an HTML alt attribute.", 0),
            # Q20 – CSP default-src 'self'
            (77,  20, "A", "All HTTP requests, upgrading them to HTTPS automatically.", 0),
            (78,  20, "B", "Loading scripts, styles, and other resources from external domains.", 1),
            (79,  20, "C", "SQL injection attempts originating from the frontend.", 0),
            (80,  20, "D", "Inline CSS styles defined directly in style attributes.", 0),
            # Q21 – textContent vs innerHTML
            (81,  21, "A", "innerText, but only when the element is visible in the viewport.", 0),
            (82,  21, "B", "textContent, which inserts raw text without parsing HTML or executing scripts.", 1),
            (83,  21, "C", "nodeValue, which strips all formatting before insertion.", 0),
            (84,  21, "D", "outerHTML, which replaces the element itself rather than its content.", 0),
            # Q22 – OR '1'='1' --
            (85,  22, "A", "The database rejects the query because of the apostrophe syntax error.", 0),
            (86,  22, "B", "Only the username field is ignored; the password check still runs.", 0),
            (87,  22, "C", "The injected OR clause makes the WHERE condition always true, returning all rows.", 1),
            (88,  22, "D", "The -- comment has no effect in most databases.", 0),
            # Q23 – correct parameterized query in Python
            (89,  23, "A", "cursor.execute(\"SELECT * FROM users WHERE username = '\" + username + \"'\")", 0),
            (90,  23, "B", "cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")", 0),
            (91,  23, "C", "cursor.execute(\"SELECT * FROM users WHERE username = %s\", (username,))", 1),
            (92,  23, "D", "cursor.execute(\"SELECT * FROM users WHERE username = \" + repr(username))", 0),
            # Q24 – stacked query injection
            (93,  24, "A", "Union-based injection, appending results from another table.", 0),
            (94,  24, "B", "Stacked query injection, executing a second destructive statement after a semicolon.", 1),
            (95,  24, "C", "Blind boolean injection, inferring data through true/false responses.", 0),
            (96,  24, "D", "Error-based injection, triggering database errors to leak schema information.", 0),
            # Q25 – frontend-only length limits
            (97,  25, "A", "Frontend limits are enforced by the browser and cannot be bypassed by normal users.", 0),
            (98,  25, "B", "Attackers can send requests directly to the server using tools like curl, bypassing all frontend controls.", 1),
            (99,  25, "C", "Length limits are sufficient because SQL injection payloads are always long.", 0),
            (100, 25, "D", "The browser re-validates input after submission, catching any tampering.", 0),
            # Q26 – blind boolean SQL injection
            (101, 26, "A", "Union-based injection.", 0),
            (102, 26, "B", "Error-based injection.", 0),
            (103, 26, "C", "Blind boolean-based injection.", 1),
            (104, 26, "D", "Out-of-band injection.", 0),
            # Q27 – UNION SELECT credential exfiltration
            (105, 27, "A", "Deleting all rows from the products table.", 0),
            (106, 27, "B", "Appending results from the users table to the product query response to steal credentials.", 1),
            (107, 27, "C", "Updating the users table with new passwords.", 0),
            (108, 27, "D", "Triggering a time delay to perform a denial-of-service attack.", 0),
            # Q28 – allowlist for dynamic column names
            (109, 28, "A", "Wrap the column name in single quotes inside the query string.", 0),
            (110, 28, "B", "Validate the column name against a hardcoded allowlist of permitted values before interpolating it.", 1),
            (111, 28, "C", "Use double quotes around the column name in all databases.", 0),
            (112, 28, "D", "Hash the column name before inserting it into the query.", 0),
            # Q29 – why CSRF tokens work
            (113, 29, "A", "Stored in a third-party cookie that attacker sites can freely read.", 0),
            (114, 29, "B", "A secret value tied to the user's session that an attacker on a different origin cannot read or predict.", 1),
            (115, 29, "C", "Encrypted with the server's private key so only HTTPS connections can use it.", 0),
            (116, 29, "D", "Regenerated every millisecond so it always expires before an attacker can use it.", 0),
            # Q30 – img tag GET-based CSRF
            (117, 30, "A", "The attacker has stolen the user's session cookie via XSS beforehand.", 0),
            (118, 30, "B", "The browser automatically sends the user's cookies with the GET request because the user is already logged in.", 1),
            (119, 30, "C", "The img tag disables HTTPS certificate checking.", 0),
            (120, 30, "D", "GET requests bypass the browser's same-origin policy entirely.", 0),
            # Q31 – SameSite cookie attribute
            (121, 31, "A", "HttpOnly", 0),
            (122, 31, "B", "Secure", 0),
            (123, 31, "C", "SameSite=Strict", 1),
            (124, 31, "D", "Domain=self", 0),
            # Q32 – POST alone does not stop CSRF
            (125, 32, "A", "POST requests are blocked by all modern browsers when sent cross-origin.", 0),
            (126, 32, "B", "Attackers can use a hidden HTML form with method=POST on their own page to send cross-origin POST requests.", 1),
            (127, 32, "C", "POST requests require HTTPS, which prevents cross-origin submission.", 0),
            (128, 32, "D", "POST bodies are never sent with cookies attached.", 0),
            # Q33 – Double Submit Cookie pattern
            (129, 33, "A", "Storing two copies of the session cookie for redundancy.", 0),
            (130, 33, "B", "Setting a random token in both a cookie and a request parameter, then verifying they match server-side without needing session storage.", 1),
            (131, 33, "C", "Requiring users to submit their password a second time on sensitive actions.", 0),
            (132, 33, "D", "Issuing two separate session tokens that must both be valid for a request to succeed.", 0),
            # Q34 – JSON Content-Type and CSRF
            (133, 34, "A", "Yes, because browsers never send cross-origin requests with a JSON Content-Type.", 0),
            (134, 34, "B", "No, because a CORS misconfiguration or browser change could still allow the request, and CSRF tokens provide defence-in-depth.", 1),
            (135, 34, "C", "Yes, because JSON payloads are always encrypted by the browser before transmission.", 0),
            (136, 34, "D", "No, because Content-Type headers are ignored by the server for API routes.", 0),
            # Q35 – SameSite=Strict sending context
            (137, 35, "A", "A cross-origin iframe embedding the site.", 0),
            (138, 35, "B", "A third-party page with an img tag pointing to the site.", 0),
            (139, 35, "C", "A direct navigation where the user types the site URL into the browser address bar.", 1),
            (140, 35, "D", "An external site that redirects to the site via a 302 response.", 0),
        ]
        connection.executemany(
            """
            INSERT INTO answer_options (id, question_id, label, option_text, is_correct)
            VALUES (?, ?, ?, ?, ?);
            """,
            new_options,
        )

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
    print(f"Database seeded at {DB_PATH}")
