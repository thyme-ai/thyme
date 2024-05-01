import requests
from flask import session
from datetime import datetime, date, time
from app.functions.google_calendar_api.get_users_current_timestamp_and_timezone import get_users_current_timestamp_and_timezone
from app.functions.helpers import get_user_by_email

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
EARLIEST_START_TIME = time(7, 0, 0) # TODO - replace with user's wake time
LATEST_END_TIME = time(11, 0, 0)    # TODO - replace with users's sleep time
CALENDAR_ID = 'primary'
# GROUP_EXPANSION_MAX = 1           # TODO - enable looking for freeBusy info across multiple calendars
# CALENDAR_EXPANSION_MAX = 1          




# Gets an array of free times given a day timestamp in RFC3339 format
def get_free_times(day):
    datetime_obj = datetime.strptime(day, DATETIME_FORMAT)
    date = datetime_obj.day
    timezone = datetime_obj.timezone

    timeMin = datetime.combine(date, EARLIEST_START_TIME, timezone)
    timeMax = datetime.combine(date, LATEST_END_TIME, timezone)

    busy_times = requests.post(
        "https://www.googleapis.com/calendar/v3/freeBusy",
        {
            "timeMin": timeMin,
            "timeMax": timeMax,
            "timeZone": timezone,
            # "groupExpansionMax": GROUP_EXPANSION_MAX,        # optional
            # "calendarExpansionMax": CALENDAR_EXPANSION_MAX,  # optional
            "items": [
                {
                "id": email
                }
            ]
        }   
    )

    print(busy_times)
