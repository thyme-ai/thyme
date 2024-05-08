from flask import Blueprint, redirect, request, session, url_for
from os import environ
from dotenv import load_dotenv
import json
import requests
import google_auth_oauthlib.flow
from app.functions.gcal.helpers.user import credentials_to_dict, get_email_from_google, get_user_from_google, get_timezone_from_google
from app.functions.thyme.helpers.user import create_user, get_user_from_thyme
bp = Blueprint("session", __name__, url_prefix="/session")

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",  # edit events in all your calendars (you cant edit/share/delete calendars)
    "https://www.googleapis.com/auth/userinfo.email",   # get user's email address
    "https://www.googleapis.com/auth/userinfo.profile", # get user's email address
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

  # Create Google Auth Flow object
  flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES)
  # flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=GOOGLE_CLIENT_CONFIG, scopes=SCOPES, state=state )

  # Set URL to redirect to after authorization
  flow.redirect_uri = url_for('session.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url 
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials

  # Get user's email from Google
  email = get_email_from_google(credentials)

  # Store credentials & email in Flask session
  session['credentials'] = credentials_to_dict(credentials)
  session['email'] = email

  # Check to see if user exists in Thyme database
  try: 
    get_user_from_thyme(email)

  # If user doesn't exist, create user in Thyme database
  except:
    user = get_user_from_google(credentials)
    timezone = get_timezone_from_google(credentials)
    first_name = user['given_name']
    last_name = user['family_name']
    profile_picture = user['picture']

    create_user(email, first_name, last_name, profile_picture, timezone)
  return redirect(url_for('home.assistant'))


# ----------------
# LOGOUT
# ----------------
@bp.route('/logout')
def logout():
  if 'credentials' not in session: 
    return redirect(url_for("home.index"))
  
  # Revoke credentails from Google Auth
  requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': session['credentials']['token']},
      headers = {'content-type': 'application/x-www-form-urlencoded'})
  
  # Delete credentials from Flask session
  if 'credentials' in session:
    del session['credentials']
    del session['email']

  return redirect(url_for("home.index"))
