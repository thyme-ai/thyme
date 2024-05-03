from datetime import datetime, date, time
from app.functions.google_calendar_api.get_users_current_timestamp_and_timezone import get_users_current_timestamp_and_timezone
from app.functions.helpers import get_user_by_email
from flask import session

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'
EARLIEST_START_TIME = time(7, 0, 0) # TODO - replace with user's wake time
LATEST_END_TIME = time(22, 0, 0)    # TODO - replace with users's sleep time
CALENDAR_ID = 'primary'
APOLOGY_STRING = "Sorry, I'm not able to do that yet."
# GROUP_EXPANSION_MAX = 1           # TODO - enable looking for freeBusy info across multiple calendars
# CALENDAR_EXPANSION_MAX = 1          


# ------------
# CREATE
# ------------
def insert_event(service, args):
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
def get_event(service, eventId):
    return APOLOGY_STRING


def list_events(service, args):
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


def get_busy_times(service, day):
    user = get_user_by_email(session['email'])
    email = user.email
    timezone = user.timezone

    datetime_obj = datetime.strptime(day, DATETIME_FORMAT)
    date = datetime_obj.date()

    tz = datetime_obj.tzinfo
    time_min = datetime.combine(date, EARLIEST_START_TIME, tz).isoformat()
    time_max = datetime.combine(date, LATEST_END_TIME, tz).isoformat()

    body =  {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": timezone,
            # "groupExpansionMax": GROUP_EXPANSION_MAX,        # optional
            # "calendarExpansionMax": CALENDAR_EXPANSION_MAX,  # optional
            "items": [{ "id": email }]
        }   
    
    busy_times = service.freebusy().query(body=body).execute()
    return busy_times


# ------------
# UPDATE
# ------------
def update_event(service, args):
    return APOLOGY_STRING


# ------------
# DELETE
# ------------
def delete_event(service, eventId):
      return APOLOGY_STRING

