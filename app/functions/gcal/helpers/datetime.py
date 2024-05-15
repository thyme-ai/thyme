from app.constants.general import DATETIME_FORMAT
from google.auth.transport.requests import AuthorizedSession
from datetime import timezone, timedelta
import pytz
from datetime import datetime

SECONDS_PER_HOUR = 3600

# --------------
# FROM GOOGLE
# --------------
def get_timezone_from_google(credentials): 
   timezone_object = AuthorizedSession(credentials).get('https://www.googleapis.com/calendar/v3/users/me/settings/timezone').json()
   return timezone_object['value']


def get_users_current_timestamp_and_timezone(user):
    timezone_object = get_timezone_object_from_string(user.timezone)
    return datetime.now(timezone_object)     


# ----------------------
# DATETIME CONVERSIONS
# ----------------------
def get_datetime_object_from_day_time_and_timezone(day, time, timezone):
    datetime_string = datetime.combine(day, time, timezone).isoformat()
    return get_datetime_object(datetime_string)


def get_datetime_string(datetime_object):
    return datetime.strftime(datetime_object, DATETIME_FORMAT)


def get_datetime_object(datetime_string):
    return datetime.strptime(datetime_string, DATETIME_FORMAT)


def get_timezone_object_from_string(timezone_string):
    timezone_dt = pytz.timezone(timezone_string)                     # string to timezone
    utc_offset = timezone_dt.utcoffset(pytz.datetime.datetime.now()) # timezone to utc offset 
    hours_from_utc = utc_offset.total_seconds() / SECONDS_PER_HOUR   # utc offset to hours
    return timezone(timedelta(hours=hours_from_utc))                 # hours to timezone object


# ---------------------
# EASY TO READ STRINGS 
# ----------------------
def get_easy_read_time(dt):
    if type(dt) is str:
        dt = datetime.strptime(dt, DATETIME_FORMAT)
    return  datetime.strftime(dt, "%I %p on %m/%d").lstrip("0")
