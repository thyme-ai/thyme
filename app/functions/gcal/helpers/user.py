from google.auth.transport.requests import AuthorizedSession
from datetime import datetime, timezone, timedelta
from flask import session, redirect, url_for
import google.oauth2.credentials
import pytz

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


def get_timezone_from_google(credentials): 
   timezone_object = AuthorizedSession(credentials).get('https://www.googleapis.com/calendar/v3/users/me/settings/timezone').json()
   return timezone_object['value']


# -----------------------------------------------
# CONVERT TIMEZONE TO GOOGLE CALENDAR API FORMAT
# -----------------------------------------------
def get_users_current_timestamp_and_timezone(user):
    # get timezone from string version of timezone (e.g. "America/Los_Angeles")
    timezone_name = user.timezone
    timezone_dt = pytz.timezone(timezone_name)

    # get offset from UTC 
    utc_offset = timezone_dt.utcoffset(pytz.datetime.datetime.now()) 

    # convert offset to hours
    hours_from_utc = utc_offset.total_seconds() / SECONDS_PER_HOUR

    # convert to timezone
    timezone_user = timezone(timedelta(hours=hours_from_utc))
    now = datetime.now(timezone_user)
    return now