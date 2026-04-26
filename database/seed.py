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
            (1,  1, "Spot Phishing Red Flags",      "Identify urgent language, spoofed domains, and unusual asks.",         "phishing-red-flags",    1),
            (2,  1, "Safe Link Handling",            "Inspect links and attachments before taking action.",                  "safe-link-handling",    2),
            (3,  2, "Strong Password Habits",        "Build resilient password and passphrase routines.",                    "strong-password-habits", 1),
            (4,  2, "MFA and Recovery",              "Use multi-factor authentication and secure recovery flows.",           "mfa-and-recovery",      2),
            (5,  3, "Cross-Site Scripting",          "Understand how XSS attacks work and how to prevent them.",            "xss",                   1),
            (6,  3, "SQL Injection",                 "Learn how attackers exploit unsanitized database queries.",           "sql-injection",          2),
            (7,  3, "Cross-Site Request Forgery",    "Detect and defend against forged cross-origin requests.",             "csrf",                  3),
            (8,  1, "Phishing",                      "Recognize fake emails and messages designed to steal your credentials.", "phishing",             5),
            (9,  1, "Social Engineering",            "Spot psychological manipulation tactics used to trick people.",        "social-engineering",    6),
            (10, 1, "Auth & Passwords",              "Build strong password habits and use multi-factor authentication.",    "auth-passwords",        7),
            (11, 1, "Sessions",                      "Understand session tokens and how attackers can hijack them.",         "sessions",              8),
        ]
        connection.executemany(
            """
            INSERT INTO modules (id, track_id, title, description, topic_key, order_index)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            modules,
        )

        quizzes = [
            (1,  1,  "Phishing Basics Quiz",       "Test your understanding of common phishing indicators."),
            (2,  2,  "Link Safety Quiz",            "Practice decisions for URLs and attachments."),
            (3,  3,  "Password Security Quiz",      "Assess your password hygiene and storage decisions."),
            (4,  4,  "MFA Essentials Quiz",         "Verify your understanding of MFA and account recovery."),
            (5,  5,  "XSS Fundamentals Quiz",       "Test your knowledge of cross-site scripting vulnerabilities."),
            (6,  6,  "SQL Injection Quiz",          "Assess your understanding of SQL injection risks and defenses."),
            (7,  7,  "CSRF Defense Quiz",           "Verify your grasp of cross-site request forgery protections."),
            (8,  8,  "Phishing Quiz",               "Test your ability to spot phishing indicators."),
            (9,  9,  "Social Engineering Quiz",     "Identify manipulation tactics and safe responses."),
            (10, 10, "Auth & Passwords Quiz",       "Assess your password hygiene and MFA knowledge."),
            (11, 11, "Sessions Quiz",               "Check your understanding of session security."),
        ]
        connection.executemany(
            "INSERT INTO quizzes (id, module_id, title, description) VALUES (?, ?, ?, ?);",
            quizzes,
        )

        # ── HEAD beginner questions (quiz_ids 1-4) and developer questions (quiz_ids 5-7) ──
        questions = [
            (1,  1, "Which sign is most likely phishing?", 1),
            (2,  1, "What should you do with an urgent payment email from a new sender?", 2),
            (3,  2, "Before clicking a shortened URL, you should:", 1),
            (4,  2, "An attachment from an unknown sender should be:", 2),
            (5,  3, "Which password is strongest?", 1),
            (6,  3, "Where is it safest to store passwords?", 2),
            (7,  4, "What is the main benefit of MFA?", 1),
            (8,  4, "Recovery codes should be:", 2),
            # XSS (quiz 5)
            (9,  5, "Which of the following is the most effective defense against stored XSS?", 1),
            (10, 5, "An attacker injects <script>document.cookie</script> into a comment field. What is the likely goal?", 2),
            # SQL Injection (quiz 6)
            (11, 6, "Which coding practice best prevents SQL injection?", 1),
            (12, 6, "A login form accepts ' OR '1'='1 as a password and grants access. What is the root cause?", 2),
            # CSRF (quiz 7)
            (13, 7, "What is the primary purpose of a CSRF token?", 1),
            (14, 7, "Which HTTP request type is most commonly exploited in CSRF attacks?", 2),
            # XSS extended (quiz 5)
            (15, 5, "Which HTML attribute is most commonly abused to execute inline XSS payloads?", 3),
            (16, 5, "A developer writes: element.innerHTML = userInput; What is wrong with this?", 4),
            (17, 5, "What does a DOM-based XSS attack manipulate that stored/reflected XSS does not?", 5),
            (18, 5, "A page renders: <img src=\"x\" onerror=\"stealCookies()\"> from user input. What type of XSS is this if the payload is saved in the database?", 6),
            (19, 5, "Which output context requires JavaScript-specific escaping rather than just HTML escaping?", 7),
            (20, 5, "A Content Security Policy header is set to: default-src 'self'. What does this prevent?", 8),
            (21, 5, "Which property should replace innerHTML when inserting plain text content safely?", 9),
            # SQL Injection extended (quiz 6)
            (22, 6, "Given this query:\nSELECT * FROM users WHERE username = 'INPUT';\n\nUser enters: ' OR '1'='1' --\n\nWhat is the effect?", 3),
            (23, 6, "Which of the following parameterized query examples correctly prevents SQL injection in Python?", 4),
            (24, 6, "An attacker enters: 1; DROP TABLE orders; --\ninto an order ID field. What class of SQL injection is this?", 5),
            (25, 6, "A login form is protected by input length limits on the frontend only. Why is this insufficient?", 6),
            (26, 6, "Which SQL injection technique is used when the application returns no visible output but responds differently based on true/false conditions?", 7),
            (27, 6, "Given:\nSELECT * FROM products WHERE id = INPUT;\n\nAttacker enters: 1 UNION SELECT username, password, null, null FROM users --\n\nWhat is the attacker attempting?", 8),
            (28, 6, "What is the safest way to handle a dynamic column name when parameterized queries cannot be used for that value?", 9),
            # CSRF extended (quiz 7)
            (29, 7, "A CSRF token is effective because it is:", 3),
            (30, 7, "An attacker hosts a page with:\n<img src=\"https://bank.com/transfer?to=attacker&amount=1000\">\nWhy does this work as a CSRF attack?", 4),
            (31, 7, "Which cookie attribute prevents it from being sent on cross-origin requests triggered by third-party pages?", 5),
            (32, 7, "A developer says 'We use POST for all state changes so we are safe from CSRF.' Why is this incorrect?", 6),
            (33, 7, "What is the Double Submit Cookie pattern used for in CSRF defense?", 7),
            (34, 7, "An API accepts only JSON and requires the Content-Type: application/json header. Does this fully protect against CSRF?", 8),
            (35, 7, "Which of the following request origins would a correctly configured SameSite=Strict cookie be sent with?", 9),
            # ── Teammate beginner questions remapped to quiz_ids 8-11 ──────────
            # Phishing (quiz 8)
            (200, 8, "Which of these is the strongest sign of a phishing email?", 1),
            (201, 8, "An email from 'support@paypa1.com' asks you to verify your account. What do you do?", 2),
            (202, 8, "What is 'spear phishing'?", 3),
            (203, 8, "You get: 'You won $1,000! Click now — offer expires in 1 hour!' This is most likely:", 4),
            # Social Engineering (quiz 9)
            (204, 9, "What is the primary goal of a social engineering attack?", 1),
            (205, 9, "Someone calls claiming to be IT support and asks for your password. You should:", 2),
            (206, 9, "What is 'pretexting'?", 3),
            (207, 9, "Which behavior is a classic social engineering red flag?", 4),
            # Auth & Passwords (quiz 10)
            (208, 10, "Which password is the strongest?", 1),
            (209, 10, "What is the safest way to store your passwords?", 2),
            (210, 10, "What is the main benefit of multi-factor authentication (MFA)?", 3),
            (211, 10, "A site you use just had a data breach. What should you do first?", 4),
            # Sessions (quiz 11)
            (212, 11, "What is a session cookie?", 1),
            (213, 11, "You finish using a public library computer to check email. You should:", 2),
            (214, 11, "Session hijacking happens when:", 3),
            (215, 11, "Which practice best protects your active sessions?", 4),
        ]
        connection.executemany(
            "INSERT INTO questions (id, quiz_id, prompt, order_index) VALUES (?, ?, ?, ?);",
            questions,
        )

        # ── Options for HEAD beginner questions (question_ids 1-14) ──────────
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
            # XSS extended – questions 15-21
            (57,  15, "A", "onerror, onclick, and other event handler attributes.", 1),
            (58,  15, "B", "The href attribute on anchor tags only.", 0),
            (59,  15, "C", "The class attribute on div elements.", 0),
            (60,  15, "D", "The alt attribute on image elements.", 0),
            (61,  16, "A", "innerHTML only works with div elements and throws errors elsewhere.", 0),
            (62,  16, "B", "It parses and renders HTML including script tags and event handlers from userInput.", 1),
            (63,  16, "C", "innerHTML is deprecated and should be replaced with outerHTML.", 0),
            (64,  16, "D", "It converts special characters to Unicode automatically, preventing injection.", 0),
            (65,  17, "A", "The server database, persisting the payload for all future visitors.", 0),
            (66,  17, "B", "The HTTP response body returned directly by the server.", 0),
            (67,  17, "C", "The client-side DOM directly, using sources like location.hash or document.referrer.", 1),
            (68,  17, "D", "The browser cache, replaying payloads on repeat visits.", 0),
            (69,  18, "A", "Reflected XSS, because the payload came from a URL parameter.", 0),
            (70,  18, "B", "Stored XSS, because the payload is persisted in the database and served to other users.", 1),
            (71,  18, "C", "DOM-based XSS, because it manipulates an HTML element attribute.", 0),
            (72,  18, "D", "Self XSS, because only the attacker who entered it is affected.", 0),
            (73,  19, "A", "Inside an HTML <p> tag body.", 0),
            (74,  19, "B", "Inside a JavaScript string variable: var name = 'USER_INPUT';", 1),
            (75,  19, "C", "Inside an HTML title element.", 0),
            (76,  19, "D", "Inside an HTML alt attribute.", 0),
            (77,  20, "A", "All HTTP requests, upgrading them to HTTPS automatically.", 0),
            (78,  20, "B", "Loading scripts, styles, and other resources from external domains.", 1),
            (79,  20, "C", "SQL injection attempts originating from the frontend.", 0),
            (80,  20, "D", "Inline CSS styles defined directly in style attributes.", 0),
            (81,  21, "A", "innerText, but only when the element is visible in the viewport.", 0),
            (82,  21, "B", "textContent, which inserts raw text without parsing HTML or executing scripts.", 1),
            (83,  21, "C", "nodeValue, which strips all formatting before insertion.", 0),
            (84,  21, "D", "outerHTML, which replaces the element itself rather than its content.", 0),
            # SQL Injection extended – questions 22-28
            (85,  22, "A", "The database rejects the query because of the apostrophe syntax error.", 0),
            (86,  22, "B", "Only the username field is ignored; the password check still runs.", 0),
            (87,  22, "C", "The injected OR clause makes the WHERE condition always true, returning all rows.", 1),
            (88,  22, "D", "The -- comment has no effect in most databases.", 0),
            (89,  23, "A", "cursor.execute(\"SELECT * FROM users WHERE username = '\" + username + \"'\")", 0),
            (90,  23, "B", "cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")", 0),
            (91,  23, "C", "cursor.execute(\"SELECT * FROM users WHERE username = %s\", (username,))", 1),
            (92,  23, "D", "cursor.execute(\"SELECT * FROM users WHERE username = \" + repr(username))", 0),
            (93,  24, "A", "Union-based injection, appending results from another table.", 0),
            (94,  24, "B", "Stacked query injection, executing a second destructive statement after a semicolon.", 1),
            (95,  24, "C", "Blind boolean injection, inferring data through true/false responses.", 0),
            (96,  24, "D", "Error-based injection, triggering database errors to leak schema information.", 0),
            (97,  25, "A", "Frontend limits are enforced by the browser and cannot be bypassed by normal users.", 0),
            (98,  25, "B", "Attackers can send requests directly to the server using tools like curl, bypassing all frontend controls.", 1),
            (99,  25, "C", "Length limits are sufficient because SQL injection payloads are always long.", 0),
            (100, 25, "D", "The browser re-validates input after submission, catching any tampering.", 0),
            (101, 26, "A", "Union-based injection.", 0),
            (102, 26, "B", "Error-based injection.", 0),
            (103, 26, "C", "Blind boolean-based injection.", 1),
            (104, 26, "D", "Out-of-band injection.", 0),
            (105, 27, "A", "Deleting all rows from the products table.", 0),
            (106, 27, "B", "Appending results from the users table to the product query response to steal credentials.", 1),
            (107, 27, "C", "Updating the users table with new passwords.", 0),
            (108, 27, "D", "Triggering a time delay to perform a denial-of-service attack.", 0),
            (109, 28, "A", "Wrap the column name in single quotes inside the query string.", 0),
            (110, 28, "B", "Validate the column name against a hardcoded allowlist of permitted values before interpolating it.", 1),
            (111, 28, "C", "Use double quotes around the column name in all databases.", 0),
            (112, 28, "D", "Hash the column name before inserting it into the query.", 0),
            # CSRF extended – questions 29-35
            (113, 29, "A", "Stored in a third-party cookie that attacker sites can freely read.", 0),
            (114, 29, "B", "A secret value tied to the user's session that an attacker on a different origin cannot read or predict.", 1),
            (115, 29, "C", "Encrypted with the server's private key so only HTTPS connections can use it.", 0),
            (116, 29, "D", "Regenerated every millisecond so it always expires before an attacker can use it.", 0),
            (117, 30, "A", "The attacker has stolen the user's session cookie via XSS beforehand.", 0),
            (118, 30, "B", "The browser automatically sends the user's cookies with the GET request because the user is already logged in.", 1),
            (119, 30, "C", "The img tag disables HTTPS certificate checking.", 0),
            (120, 30, "D", "GET requests bypass the browser's same-origin policy entirely.", 0),
            (121, 31, "A", "HttpOnly", 0),
            (122, 31, "B", "Secure", 0),
            (123, 31, "C", "SameSite=Strict", 1),
            (124, 31, "D", "Domain=self", 0),
            (125, 32, "A", "POST requests are blocked by all modern browsers when sent cross-origin.", 0),
            (126, 32, "B", "Attackers can use a hidden HTML form with method=POST on their own page to send cross-origin POST requests.", 1),
            (127, 32, "C", "POST requests require HTTPS, which prevents cross-origin submission.", 0),
            (128, 32, "D", "POST bodies are never sent with cookies attached.", 0),
            (129, 33, "A", "Storing two copies of the session cookie for redundancy.", 0),
            (130, 33, "B", "Setting a random token in both a cookie and a request parameter, then verifying they match server-side without needing session storage.", 1),
            (131, 33, "C", "Requiring users to submit their password a second time on sensitive actions.", 0),
            (132, 33, "D", "Issuing two separate session tokens that must both be valid for a request to succeed.", 0),
            (133, 34, "A", "Yes, because browsers never send cross-origin requests with a JSON Content-Type.", 0),
            (134, 34, "B", "No, because a CORS misconfiguration or browser change could still allow the request, and CSRF tokens provide defence-in-depth.", 1),
            (135, 34, "C", "Yes, because JSON payloads are always encrypted by the browser before transmission.", 0),
            (136, 34, "D", "No, because Content-Type headers are ignored by the server for API routes.", 0),
            (137, 35, "A", "A cross-origin iframe embedding the site.", 0),
            (138, 35, "B", "A third-party page with an img tag pointing to the site.", 0),
            (139, 35, "C", "A direct navigation where the user types the site URL into the browser address bar.", 1),
            (140, 35, "D", "An external site that redirects to the site via a 302 response.", 0),
            # ── Teammate options for questions 200-215 ────────────────────────
            # Q200
            (300, 200, "A", "An email with a professional company logo and expected context.", 0),
            (301, 200, "B", "An email demanding you click a link immediately or your account gets deleted.", 1),
            (302, 200, "C", "A newsletter from a site you subscribed to last week.", 0),
            (303, 200, "D", "A password-reset email you yourself requested.", 0),
            # Q201
            (304, 201, "A", "Click the link and log in to resolve the issue quickly.", 0),
            (305, 201, "B", "Reply with your account details to prove your identity.", 0),
            (306, 201, "C", "Navigate directly to paypal.com by typing it in your browser.", 1),
            (307, 201, "D", "Forward the email to friends as a warning.", 0),
            # Q202
            (308, 202, "A", "A phishing attack sent by physical mail.", 0),
            (309, 202, "B", "A targeted attack that uses personal info about you to seem believable.", 1),
            (310, 202, "C", "An attack that targets only email servers.", 0),
            (311, 202, "D", "Phishing conducted exclusively through phone calls.", 0),
            # Q203
            (312, 203, "A", "A legitimate prize from a company you recently purchased from.", 0),
            (313, 203, "B", "A phishing attempt using urgency and reward bait to rush you into clicking.", 1),
            (314, 203, "C", "An official government tax rebate notification.", 0),
            (315, 203, "D", "A security test sent by your IT department.", 0),
            # Q204
            (316, 204, "A", "Breaking through firewalls using exploit code.", 0),
            (317, 204, "B", "Manipulating people into revealing sensitive info or taking unsafe actions.", 1),
            (318, 204, "C", "Installing viruses on public computers.", 0),
            (319, 204, "D", "Overloading websites with traffic.", 0),
            # Q205
            (320, 205, "A", "Provide the password since the issue sounds urgent.", 0),
            (321, 205, "B", "Ask them to send an email instead and share it there.", 0),
            (322, 205, "C", "Refuse and verify their identity through official channels.", 1),
            (323, 205, "D", "Give them only the first half of your password.", 0),
            # Q206
            (324, 206, "A", "Sending emails with misleading subject lines.", 0),
            (325, 206, "B", "Creating a fabricated scenario to gain trust and extract information.", 1),
            (326, 206, "C", "Using fake pop-up windows to steal credentials.", 0),
            (327, 206, "D", "Hiding malware inside image files.", 0),
            # Q207
            (328, 207, "A", "A vendor confirming your delivery address.", 0),
            (329, 207, "B", "A colleague sharing a project status update.", 0),
            (330, 207, "C", "Someone creating extreme urgency and demanding you keep it secret.", 1),
            (331, 207, "D", "HR sending a benefits enrollment reminder.", 0),
            # Q208
            (332, 208, "A", "Summer2024", 0),
            (333, 208, "B", "P@ssword123!", 0),
            (334, 208, "C", "Blue!River!Orbit!Candle!73", 1),
            (335, 208, "D", "qwerty456", 0),
            # Q209
            (336, 209, "A", "Write them in a notebook kept at your desk.", 0),
            (337, 209, "B", "Use one memorable password across all sites.", 0),
            (338, 209, "C", "Store them in an encrypted password manager.", 1),
            (339, 209, "D", "Save them in a browser with no master password set.", 0),
            # Q210
            (340, 210, "A", "It automatically makes your passwords longer.", 0),
            (341, 210, "B", "It adds a second verification step so stolen passwords alone are not enough.", 1),
            (342, 210, "C", "It encrypts all the files on your device.", 0),
            (343, 210, "D", "It blocks all phishing emails at the server level.", 0),
            # Q211
            (344, 211, "A", "Wait to see if you start receiving spam.", 0),
            (345, 211, "B", "Change your password on that site immediately, and on any other site where you reused it.", 1),
            (346, 211, "C", "Delete the account and never use that site again.", 0),
            (347, 211, "D", "Contact the site's CEO on LinkedIn.", 0),
            # Q212
            (348, 212, "A", "A file that stores your full browsing history.", 0),
            (349, 212, "B", "A token the server gives you after login to identify your active session.", 1),
            (350, 212, "C", "An encrypted copy of your password stored on your device.", 0),
            (351, 212, "D", "A tracking pixel embedded in marketing emails.", 0),
            # Q213
            (352, 213, "A", "Just close the browser tab.", 0),
            (353, 213, "B", "Click 'Log out' on the site, then close the browser.", 1),
            (354, 213, "C", "Turn off the monitor.", 0),
            (355, 213, "D", "Clear only the download history.", 0),
            # Q214
            (356, 214, "A", "Someone correctly guesses your password.", 0),
            (357, 214, "B", "An attacker steals your session token and accesses your account without your password.", 1),
            (358, 214, "C", "You accidentally stay logged in on your own device.", 0),
            (359, 214, "D", "The server crashes and logs everyone out.", 0),
            # Q215
            (360, 215, "A", "Stay logged in on all devices permanently for convenience.", 0),
            (361, 215, "B", "Use public Wi-Fi for all banking and shopping activities.", 0),
            (362, 215, "C", "Use HTTPS websites and log out when done on shared or public devices.", 1),
            (363, 215, "D", "Disable all browser cookies so sessions can't be tracked.", 0),
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
