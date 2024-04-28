from flask import Blueprint, redirect, request, session, url_for
from os import environ
from dotenv import load_dotenv
import json
import google_auth_oauthlib.flow
from app.functions.helpers import credentials_to_dict

bp = Blueprint("session", __name__, url_prefix="/session")

SCOPES = [
    "https://www.googleapis.com/auth/calendar",         # edit calendar
    "https://www.googleapis.com/auth/userinfo.email",   # get email 
    "https://www.googleapis.com/auth/calendar.readonly" # get timezone
]

load_dotenv()
GOOGLE_CLIENT_CONFIG = json.loads(environ.get('GOOGLE_CLIENT_CONFIG'))


# ----------------
# LOGIN
# ----------------
@bp.route('/login', methods=["GET", "POST"])
def login():
  flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES )
  flow.redirect_uri = url_for('session.oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      access_type='offline',        # Enable offline access so you can refresh access token without re-prompting user for permission.
      include_granted_scopes='true' # Enable incremental authorizations
      )

  session['state'] = state 
  print('------------------')
  print('AUTH URL', authorization_url)
  return redirect(authorization_url)
  # return redirect(url_for('home.assistant'))


# ----------------
# OATH2 CALLBACK
# ----------------
@bp.route('/oauth2callback', methods=["GET", "POST"])
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = session['state']

  # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(GOOGLE_CLIENT_SECRETS_JSON, scopes=SCOPES, state=state)
  flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES )
  flow.redirect_uri = url_for('session.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session (TODO: Replace with saving to database)
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)
  return redirect(url_for('home.assistant'))


# ----------------
# LOGOUT
# ----------------
@bp.route('/logout, ', methods=["GET", "POST"])
def logout():
  if 'credentials' in session:
    del session['credentials']
  return redirect(url_for("home.index"))