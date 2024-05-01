from datetime import datetime, timezone, timedelta
import pytz

SECONDS_PER_HOUR = 3600


def get_users_current_timestamp_and_timezone(user):
    timezone_name = user.timezone
    hours_from_utc = get_hours_from_utc_from_timezone_name(timezone_name)
    timezone_user = timezone(timedelta(hours=hours_from_utc))
    now = datetime.now(timezone_user)
    return now


# Converts timezone name into offset in hrs from UTC (e.g. "America/Los_Angeles" returns 7 hours)
def get_hours_from_utc_from_timezone_name(timezone_name):
    timezone = pytz.timezone(timezone_name)
    utc_offset = timezone.utcoffset(pytz.datetime.datetime.now())   # get offset 
    hours_from_utc = utc_offset.total_seconds() / SECONDS_PER_HOUR  # convert to hours
    return hours_from_utc
