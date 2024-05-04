from datetime import datetime, date, time, timedelta
from app.functions.gcal.utils.build_google_api_service_object_with_creds import build_google_api_service_object_with_creds
from app.functions.helpers import get_user_by_email, get_easy_read_time
from flask import session

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
CALENDAR_ID = 'primary'
APOLOGY_STRING = "Sorry, I'm not able to do that yet."    


def insert_event(args):
    print('ARGS-----', args)
    service = build_google_api_service_object_with_creds()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return f"I created your event called {event.get("summary")}"
    else:
         return f"""
        {APOLOGY_STRING} Try saying something like this : 
        "Add a _____ hour long event to my calendar called _____ on _____.
        """


def insert_event_while_avoiding_conflicts(args):
    ideal_start = datetime.strptime(args['start']['dateTime'], DATETIME_FORMAT)
    ideal_end = datetime.strptime(args['end']['dateTime'], DATETIME_FORMAT)   

    print('--------------------')
    print('IDEAL START----------', ideal_start)                   

    closest_free_start = get_closest_free_start(ideal_start, ideal_end)
    duration = ideal_end - ideal_start

    args['start']['dateTime'] = datetime.strftime(closest_free_start, DATETIME_FORMAT)
    args['end']['dateTime'] = datetime.strftime(closest_free_start + duration, DATETIME_FORMAT)

    print('ARGS------', args)

    service = build_google_api_service_object_with_creds()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return f"""
        I created your event called {event.get("summary")}
        at the closest available time which was {get_easy_read_time(closest_free_start)}
        """
    else:
         return f"""
        {APOLOGY_STRING} Try saying something like this : 
        "Add a _____ hour long event to my calendar called _____ on _____.
        """



def list_events(args):
    service = build_google_api_service_object_with_creds()
    params = {"calendarId": "primary"}
    for key in args.keys():
        params[key] = args.get(key)
    events = service.events().list(**params).execute()['items']

    if events:
        intro = "Here are the events on your calendar:"
        event_summaries = []

        for event in events:
            summary = event.get('summary')
            start = event.get('start').get('dateTime')
            event_summaries.append(f"{summary} at {get_easy_read_time(start)}")

        return f"{intro} {(", ").join(event_summaries)}"
    
    return f"""
        {APOLOGY_STRING} Try saying: "What's on my calendar today?" or 
        "Give me a list of events on my calendar called _____"
        """


def get_busy_times(day):
    busy_times_obj = get_busy_times_within_awake_hours(day)
    busy_times_strings = map(lambda x: f"{get_easy_read_time(x['start'])} to {get_easy_read_time(x['end'])}", busy_times_obj)
    busy_times_joined_string = (", ").join(busy_times_strings)

    if busy_times_joined_string:
        return f"""
            Here is a list of times 
            within your preferred wake & sleep hours, 
            when you are busy: {busy_times_joined_string}
        """
    else:
        return "You're free all day!"
    

# ------------------------
# NOT SUPPORTED YET 
# ------------------------
def get_event(eventId):
    return APOLOGY_STRING


def update_event(args):
    return APOLOGY_STRING


def delete_event(eventId):
      return APOLOGY_STRING


# ------------------------
# HELPERS
# ------------------------
def get_busy_times_within_awake_hours(day):
    user = get_user_by_email(session['email'])
    email = user.email
    timezone = user.timezone

    if type(day) is datetime:
        day = datetime.strftime(day, DATETIME_FORMAT)

    datetime_obj = datetime.strptime(day, DATETIME_FORMAT)
    date = datetime_obj.date()

    tz = datetime_obj.tzinfo
    time_min = datetime.combine(date, user.wake_time, tz).isoformat()
    time_max = datetime.combine(date, user.sleep_time, tz).isoformat()

    body =  {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": timezone,
            "items": [{ "id": email }]
        }   
    
    service = build_google_api_service_object_with_creds()
    response = service.freebusy().query(body=body).execute()
    busy_times_obj = response['calendars'][email]['busy']
    return busy_times_obj



def get_closest_free_start(ideal_start, ideal_end):

    if type(ideal_start) == str:
        ideal_start = datetime.strptime(ideal_start, DATETIME_FORMAT)
        ideal_end = datetime.strptime(ideal_end, DATETIME_FORMAT)

    max_delta = timedelta(minutes=8*60)
    increment = timedelta(minutes=30)

    # get ranges during which user is busy 
    busy_ranges = get_busy_times_within_awake_hours(ideal_start)

    # get users awake hours 
    user = get_user_by_email(session['email'])

    
    if type(ideal_start) is datetime:
        ideal_start = datetime.strftime(ideal_start, DATETIME_FORMAT)
    
    datetime_obj = datetime.strptime(ideal_start, DATETIME_FORMAT)
    date = datetime_obj.date()
    tz = datetime_obj.tzinfo
    awake_range = {
        'start': datetime.combine(date, user.wake_time, tz).isoformat(), 
        'end': datetime.combine(date, user.sleep_time, tz).isoformat()
    }

    ideal_start = datetime.strptime(ideal_start, DATETIME_FORMAT)

    print('-------------------')
    print('BUSY RANGES', busy_ranges)

    closest_start = ideal_start
    delta = timedelta(minutes=0)
    while (delta < max_delta):
    
        starts = [ideal_start + delta, ideal_start - delta]
        ends = [ideal_end + delta, ideal_end - delta]

        for i in range(len(starts)):
            print('----------------------')
            print(f'(i = {i}) ----Checking to see if {get_easy_read_time(starts[i])} works...')
            if time_is_available(busy_ranges, starts[i], ends[i]) and time_is_within_wake_hours(awake_range, starts[i], ends[i]): 
                closest_start = starts[i]
                print('🎉FOUND A TIME------', closest_start)
                return closest_start

        delta += increment

    return closest_start
            
        

def time_is_available(busy_ranges, target_start, target_end):
    start_and_end_are_free = False
    user = get_user_by_email(session['email'])

    # iterate over all busy ranges for that day 
    for busy_range in busy_ranges:
        start = datetime.strptime(busy_range['start'], DATETIME_FORMAT)
        end = datetime.strptime(busy_range['end'], DATETIME_FORMAT)

        # check to see if target_start or target_end fall within the busy range
        start_in_busy_range = target_in_range(target_start, start, end)
        end_in_busy_range = target_in_range(target_end, start, end)

        # if either the start or the end is in the busy range
        if (start_in_busy_range or end_in_busy_range): 
            print('❌ Busy')
            return False      
    return True


def time_is_within_wake_hours(awake_range, target_start, target_end):
    start = datetime.strptime(awake_range['start'], DATETIME_FORMAT)
    end = datetime.strptime(awake_range['end'], DATETIME_FORMAT)

    # check to see if target_start or target_end fall within the waking range
    start_in_awake_range = target_in_range(target_start, start, end)
    end_in_awake_range = target_in_range(target_end, start, end)

    # if either the start or the end is NOT in the awake range
    if (not start_in_awake_range or not end_in_awake_range): 
        print('⏰ Outside of awake hours')
        return False   
    
    return True 


def target_in_range(target, start, end):
    if target > start and target < end:
        return True
    else: 
        return False








