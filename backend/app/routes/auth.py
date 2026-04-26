from flask import Blueprint, redirect, request, url_for, session, jsonify
from oauthlib.oauth2 import WebApplicationClient
import json
import os
import requests

from ..db.connection import get_db

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Make sure to use this environment variable in production!
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_google_provider_cfg():
    return json.loads(
        requests.get(GOOGLE_DISCOVERY_URL).text
    )

@auth_bp.route("/login")
def login():
    # If user is already logged in, redirect to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))
    
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_bp.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(token_response.text)

    # Now that we have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure we are logged in to the verified account
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        users_id = userinfo_response.json()["sub"]
    else:
        return jsonify({"error": "User email not available or not verified by Google."}), 400

    # Create or get user in our database
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE oauth_provider = 'google' AND oauth_id = ?",
        (users_id,),
    ).fetchone()

    if user is None:
        # Insert new user
        cursor = db.execute(
            "INSERT INTO users (name, oauth_provider, oauth_id) VALUES (?, ?, ?)",
            (users_name, "google", users_id),
        )
        db.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]

    # Store user ID in session
    session["user_id"] = user_id
    session["user_name"] = users_name
    session["user_email"] = users_email

    # Redirect to dashboard or home page
    return redirect(url_for("dashboard.index"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard.index"))

@auth_bp.route("/user")
def get_user():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({
        "id": session["user_id"],
        "name": session["user_name"],
        "email": session["user_email"]
    })