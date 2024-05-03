from app.models import db, User, Habit
from flask import redirect, session, url_for
import google.oauth2.credentials
from datetime import datetime, time, timezone, timedelta
import pytz

SECONDS_PER_HOUR = 3600

# ------------------
# CREDENTIALS
# ------------------
def check_for_credentials():
    if 'credentials' not in session:
        return redirect(url_for("session.login"))
    creds = google.oauth2.credentials.Credentials(**session['credentials'])
    return creds


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

# ------------------
# HABITS
# ------------------
def get_habit(habit_id):
    return db.session.execute(
        db.select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one()


def get_habits():
    user_id = get_user_id_or_create_new_user()
    habits = db.session.execute(
            db.select(Habit)
            .where(Habit.user_id == user_id)
            .order_by(Habit.name)
            ).scalars().all()
    return habits


# ------------------
# USERS
# ------------------
def create_user(email, first_name, last_name, profile_picture, timezone):
    user = User(
       email = email,
       first_name = first_name,
       last_name = last_name,
       profile_picture = profile_picture,
       timezone = timezone,
       wake_time = time(hour=7, minute=0),
       sleep_time = time(hour=22, minute=0),
       )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
   return db.one_or_404(db.select(User).filter_by(email=email))


def get_user_or_create_new_user():
    email = session['email']
    try:
      user = get_user_by_email(email)
    except:
      user = create_user()    
    return user


def get_user_id_or_create_new_user():
   user = get_user_or_create_new_user()
   return user.id


# ------------------
# TIME
# ------------------
def get_easy_read_time(datetime_str):
    # Define the format string to match the input datetime string
    input_format_str = "%Y-%m-%dT%H:%M:%S%z"

    # Parse the string into a datetime object
    datetime_obj = datetime.strptime(datetime_str, input_format_str)

    # Format the datetime object into the desired string format
    output_format_str = "%I:%M %p on %m/%d/%Y"
    formatted_datetime_str = datetime_obj.strftime(output_format_str)

    return formatted_datetime_str


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