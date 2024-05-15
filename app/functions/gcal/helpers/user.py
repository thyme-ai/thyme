from app.functions.gcal.helpers.datetime import get_timezone_object_from_string
from google.auth.transport.requests import AuthorizedSession
from datetime import datetime
from flask import session, redirect, url_for
import google.oauth2.credentials

SECONDS_PER_HOUR = 3600

# ------------------
# CREDENTIALS
# ------------------
def get_credentials():
    if 'credentials' not in session:
        return redirect(url_for("home.index"))

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    return credentials


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


# ---------------------------
# GET USER INFO FROM GOOGLE
# ---------------------------
def get_email_from_google(credentials):
   user_info = AuthorizedSession(credentials).get('https://www.googleapis.com/oauth2/v3/userinfo').json()
   return user_info['email']


def get_user_from_google(credentials):
    user =  AuthorizedSession(credentials).get('https://www.googleapis.com/oauth2/v3/userinfo#profile').json()
    return user                   