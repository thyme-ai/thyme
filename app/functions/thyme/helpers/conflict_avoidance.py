from app.constants.general import DATETIME_FORMAT, MAX_DELTA, INCREMENT
from datetime import datetime, timedelta
from app.functions.gcal.utils.build_google_api_service import build_google_api_service
from app.functions.thyme.helpers.user import get_user_from_thyme
from app.functions.thyme.utils.get_easy_read_time import get_easy_read_time
from flask import session

def get_best_time_for_meeting_while_avoiding_conflicts(ideal_start, ideal_end):
    if type(ideal_start) == str:
        ideal_start = datetime.strptime(ideal_start, DATETIME_FORMAT)
        ideal_end = datetime.strptime(ideal_end, DATETIME_FORMAT)

    busy_ranges = get_busy_times_within_awake_range(ideal_start)
    awake_range = get_awake_range(ideal_start)

    best_start_time = None
    delta = timedelta(minutes=0)
    while (delta < MAX_DELTA):
        starts = [ideal_start + delta, ideal_start - delta]
        ends = [ideal_end + delta, ideal_end - delta]

        for i in range(len(starts)):
            print('----------------------')
            print(f'(i = {i}) ----Checking to see if {get_easy_read_time(starts[i])} works...')
            if time_is_available(busy_ranges, starts[i], ends[i]) and time_is_within_wake_hours(awake_range, starts[i], ends[i]): 
                best_start_time = starts[i]
                print('🎉 Found a free time within awake hours')  
                return best_start_time
        delta += INCREMENT
    return None


def time_is_available(busy_ranges, target_start, target_end):
    for busy_range in busy_ranges:
        start = datetime.strptime(busy_range['start'], DATETIME_FORMAT)
        end = datetime.strptime(busy_range['end'], DATETIME_FORMAT)

        start_in_busy_range = target_in_range(target_start, start, end)
        end_in_busy_range = target_in_range(target_end, start, end)

        start_in_target_range = target_in_range(start, target_start, target_end)
        end_in_target_range = target_in_range(end, target_start, target_end)

        if (start_in_busy_range or end_in_busy_range or start_in_target_range or end_in_target_range): 
            print('❌ Busy at this time')
            return False    
    return True


def get_busy_times_within_awake_range(day):
    user = get_user_from_thyme(session['email'])
    awake_range = get_awake_range(day)
    time_min = awake_range['start']
    time_max = awake_range['end']

    body =  {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": user.timezone,
            "items": [{ "id": user.email }]
        }   
    
    service = build_google_api_service()
    response = service.freebusy().query(body=body).execute()
    busy_times_obj = response['calendars'][user.email]['busy']
    return busy_times_obj   


def get_awake_range(day):
    user = get_user_from_thyme(session['email'])

    if type(day) is datetime:
        day = datetime.strftime(day, DATETIME_FORMAT)
    
    datetime_obj = datetime.strptime(day, DATETIME_FORMAT)
    date = datetime_obj.date()
    tz = datetime_obj.tzinfo

    awake_range = {
        'start': datetime.combine(date, user.wake_time, tz).isoformat(), 
        'end': datetime.combine(date, user.sleep_time, tz).isoformat()
    }
    return awake_range


def time_is_within_wake_hours(awake_range, target_start, target_end):
    start = datetime.strptime(awake_range['start'], DATETIME_FORMAT)
    end = datetime.strptime(awake_range['end'], DATETIME_FORMAT)

    start_in_awake_range = target_in_range(target_start, start, end)
    end_in_awake_range = target_in_range(target_end, start, end)

    if (not start_in_awake_range or not end_in_awake_range): 
        print('⏰ Outside of awake hours')
        return False  
    return True 


def target_in_range(target, start, end):
    if target > start and target < end:
        return True
    return False