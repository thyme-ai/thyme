from app.constants.general import MAX_DELTA, INCREMENT
from datetime import datetime, timedelta
from app.functions.gcal.utils.build_google_api_service import build_google_api_service
from app.functions.gcal.helpers.datetime import (
    get_datetime_string, 
    get_datetime_object, 
    get_datetime_object_from_day_time_and_timezone,
    get_users_current_timestamp_and_timezone
)
from app.functions.thyme.helpers.user import get_user_from_thyme
from app.functions.gcal.helpers.datetime import get_easy_read_time
from flask import session

def get_suggested_start_time(ideal_start, ideal_end, awake_range, busy_ranges):
    best_start_time = None
    delta = timedelta(minutes=0)

    while (delta < MAX_DELTA):
        starts = [ideal_start + delta, ideal_start - delta]
        ends = [ideal_end + delta, ideal_end - delta]

        for i in range(len(starts)):
            start = starts[i]
            end = ends[i]
            print(f'Checking to see if {get_easy_read_time(start)} works...')
            range_in_awake_range = start_or_end_in_range(start, end, awake_range['start'], awake_range['end'])
            range_in_busy_ranges = start_or_end_in_ranges(start, end, busy_ranges)

            if range_in_awake_range and not range_in_busy_ranges: 
                best_start_time = start
                print('🎉 Found a free time within awake hours\n')  
                return best_start_time
            print('❌ Busy\n')  
        delta += INCREMENT
    return None


# --------------------
# AWAKE & BUSY RANGES
# ---------------------
def get_busy_ranges_within_awake_range(dt):
    user = get_user_from_thyme(session['email'])
    awake_range = get_awake_range(dt)

    # convert awake ranges to strings for gcal request
    awake_range_start = get_datetime_string(awake_range['start'])
    awake_range_end = get_datetime_string(awake_range['end'])
    body =  {
            "timeMin": awake_range_start,
            "timeMax": awake_range_end,
            "timeZone": user.timezone,
            "items": [{ "id": user.email }]
        }   
    
    # get busy ranges from google calendar
    service = build_google_api_service()
    response = service.freebusy().query(body=body).execute()
    busy_ranges = response['calendars'][user.email]['busy']

    # convert busy_ranges to datetime objects 
    for busy_range in busy_ranges: 
        busy_range['start'] = get_datetime_object(busy_range['start'])
        busy_range['end'] = get_datetime_object(busy_range['end'])
    return busy_ranges


def get_awake_range(dt):
    user = get_user_from_thyme(session['email'])
    now = get_users_current_timestamp_and_timezone(user)
    day = dt.date()
    timezone = dt.tzinfo

    time_wake = user.wake_time
    time_sleep = user.sleep_time

    # if day is today, adjust the awake_range start to be the current time 
    if now.date() == day:
        print('🌤️ User scheduling event today, adjusting wake time \n')
        time_wake_string = now.time().strftime("%H:%M:%S")
        time_wake = datetime.strptime(time_wake_string, "%H:%M:%S").time()

    # convert sleep & wake times to datetime objects
    awake_start = get_datetime_object_from_day_time_and_timezone(day, time_wake, timezone)
    awake_end = get_datetime_object_from_day_time_and_timezone(day, time_sleep, timezone) 
    return { 
        'start': awake_start,
        'end': awake_end
    }


# ---------------
# HELPERS
# ---------------
def start_or_end_in_ranges(start, end, ranges):
    for range in ranges: 
        if start_or_end_in_range(start, end, range['start'], range['end']):
            return True
    return False


def start_or_end_in_range(start, end, range_start, range_end):
    start_in_range = (start >= range_start and start < range_end)
    end_in_range = (end > range_start and end <= range_end)
    return start_in_range or end_in_range