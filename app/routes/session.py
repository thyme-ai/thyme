from flask import Blueprint, redirect, request, session, url_for
from os import environ
from dotenv import load_dotenv
import json
import requests
import google_auth_oauthlib.flow
from app.functions.helpers import credentials_to_dict
from google.auth.transport.requests import AuthorizedSession
import google.oauth2.credentials
from app.functions.helpers import create_user, get_user_by_email

bp = Blueprint("session", __name__, url_prefix="/session")

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",  # edit events in all your calendars (you cant edit/share/delete calendars)
    "https://www.googleapis.com/auth/userinfo.email",   # get user's email address
    "https://www.googleapis.com/auth/userinfo.profile",   # get user's email address
    "https://www.googleapis.com/auth/calendar.readonly" # get calendar settings (including)
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
  return redirect(authorization_url)


# ----------------
# OATH2 CALLBACK
# ----------------
@bp.route('/oauth2callback', methods=["GET", "POST"])
def oauth2callback():
  # Specify state when creating flow in the callback so it can be verified in authorization server response.
  # state = session['state']

  # flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES, state=state )
  flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES)
  flow.redirect_uri = url_for('session.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session (TODO: Replace with saving to database)
  credentials = flow.credentials
  session["credentials"] = credentials_to_dict(credentials)

  # get users email
  user_info = AuthorizedSession(credentials).get('https://www.googleapis.com/oauth2/v3/userinfo').json()
  email = user_info['email']
  session['email'] = email

  # get user
  try: 
    get_user_by_email(email)
  except:
    # if user doesn't exist yet, get rest of user info & create user 
    profile = AuthorizedSession(credentials).get('https://www.googleapis.com/oauth2/v3/userinfo#profile').json()
    timezone_object = AuthorizedSession(credentials).get('https://www.googleapis.com/calendar/v3/users/me/settings/timezone').json()
    
    first_name = profile['given_name']
    last_name = profile['family_name']
    profile_picture = profile['picture']
    timezone = timezone_object['value']

    create_user(email, first_name, last_name, profile_picture, timezone)

  return redirect(url_for('home.assistant'))


# ----------------
# LOGOUT
# ----------------
@bp.route('/logout')
def logout():
  credentials = google.oauth2.credentials.Credentials(**session['credentials'])
  requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})
  
  if 'credentials' in session:
    del session['credentials']
    del session['email']

  return redirect(url_for("home.index"))