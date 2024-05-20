from app.constants.general import DATETIME_FORMAT
from app.constants.prompts import NON_NUMERIC_DATE_STRINGS
from google.auth.transport.requests import AuthorizedSession
from datetime import timezone, timedelta
from dateutil import parser
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


def get_easy_read_time(dt):
    if type(dt) is str:
        dt = datetime.strptime(dt, DATETIME_FORMAT)
    return  datetime.strftime(dt, "%I:%M %p on %m/%d").lstrip("0")


# -----------
# HELPERS 
# ___________
def get_first_non_numeric_date_string_in_prompt(prompt):
    prompt = prompt.lower()

    for i, string in enumerate(NON_NUMERIC_DATE_STRINGS):
        if string.lower() in prompt.lower():
            print('✅ Found a Non-Numeric Date String', string)
            return string
    return None


def get_prompt_with_non_numeric_dates_converted_to_datetime(prompt):
    non_numeric_date_string = get_first_non_numeric_date_string_in_prompt(prompt)

    if non_numeric_date_string:
        datetime_string_wrong_format = parser.parse(non_numeric_date_string)
        # datetime_obj = datetime.strftime(str(datetime_string_wrong_format), "%Y-%m-%d %H:%M:%S")
        datetime_string = datetime.strftime(datetime_string_wrong_format, "%Y-%m-%d")

        print('non numeric', non_numeric_date_string, type(non_numeric_date_string))
        print('numeric', datetime_string, type(datetime_string))

        print('PROMPT BEFORE', prompt)
        new_prompt = prompt.replace(non_numeric_date_string, datetime_string)
        print('NEW PROMPT', new_prompt)
        return new_prompt
    return prompt