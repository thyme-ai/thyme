from datetime import datetime, date, time
from app.functions.google_calendar_api.get_users_current_timestamp_and_timezone import get_users_current_timestamp_and_timezone
from app.functions.google_calendar_api.build_google_api_service_object_with_creds import build_google_api_service_object_with_creds
from app.functions.helpers import get_user_by_email, get_easy_read_time
from flask import session

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
CALENDAR_ID = 'primary'
APOLOGY_STRING = "Sorry, I'm not able to do that yet."    

# ------------
# CREATE
# ------------
def insert_event(args):
    service = build_google_api_service_object_with_creds()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return f"I created your event called {event.get("summary")}"
    else:
         return f"""
        {APOLOGY_STRING} Try saying something like this : 
        "Add a _____ hour long event to my calendar called _____ on _____.
        """

# ------------
# READ
# ------------
def get_event(eventId):
    return APOLOGY_STRING


def list_events(args):
    service = build_google_api_service_object_with_creds()
    params = {"calendarId": "primary"}
    for key in args.keys():
        params[key] = args.get(key)
    events = service.events().list(**params).execute()['items']

    if events:
        intro = "Here's a summary of the events I found:"
        event_summaries = []

        for event in events:
            summary = event.get('summary')
            start = event.get('start')

            dt_str = start.get('dateTime')
            dt_object = datetime.fromisoformat(dt_str)

            date = dt_object.date()
            time = dt_object.time()

            event_summaries.append(f"{summary} on {date} at {time}")
        return f"{intro} + {(", ").join(event_summaries)}"
    
    return f"""
        {APOLOGY_STRING} Try saying: "What's on my calendar today?" or 
        "Give me a list of events on my calendar called _____"
        """

# ----------------
# GET BUSY TIMES
# ----------------
def get_busy_times(day):
    user = get_user_by_email(session['email'])
    email = user.email
    timezone = user.timezone

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
    start_end_times = response['calendars'][email]['busy']
    busy_times = map(lambda x: f"{get_easy_read_time(x['start'])} to {get_easy_read_time(x['end'])}", start_end_times)
    busy_times_string = (", ").join(busy_times)

    if busy_times_string:
        return f"""
            Here is a list of times 
            within your preferred wake & sleep hours, 
            when you are busy: {busy_times_string}
        """
    else:
        return "You're free all day!"



# ------------
# UPDATE
# ------------
def update_event(args):
    return APOLOGY_STRING


# ------------
# DELETE
# ------------
def delete_event(eventId):
      return APOLOGY_STRING

