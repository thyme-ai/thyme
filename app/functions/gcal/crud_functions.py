from app.constants.general import APOLOGY, CALENDAR_ID, DATETIME_FORMAT
from app.functions.gcal.utils.build_google_api_service import build_google_api_service
from app.functions.thyme.helpers.conflict_avoidance import get_best_time_for_meeting_while_avoiding_conflicts
from app.functions.thyme.utils.get_easy_read_time import get_easy_read_time
from datetime import datetime

def insert_event(args):
    service = build_google_api_service()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return f"""
        I created your event called {event.get("summary")} 
        at {get_easy_read_time(event.get("start").get("dateTime"))}
        """
    else:
         return f"""
        {APOLOGY} Try saying something like this : 
        "Add a _____ hour long event to my calendar called _____ on _____.
        """


def insert_event_while_avoiding_conflicts(args):
    ideal_start = datetime.strptime(args['start']['dateTime'], DATETIME_FORMAT)
    ideal_end = datetime.strptime(args['end']['dateTime'], DATETIME_FORMAT)                 
    best_start_time = get_best_time_for_meeting_while_avoiding_conflicts(ideal_start, ideal_end)

    if not best_start_time:
        return f"""
        Sorry, I couldn't find any free times for your event
        that are within your preferred wake up & sleep times. 
        Try a different time or different day. 
        """

    duration = ideal_end - ideal_start
    args['start']['dateTime'] = datetime.strftime(best_start_time, DATETIME_FORMAT)
    args['end']['dateTime'] = datetime.strftime(best_start_time + duration, DATETIME_FORMAT)

    service = build_google_api_service()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return f"""
        I created your event called {event.get("summary")}
        at the closest available time within your preferred wake & sleep hours 
        which was {get_easy_read_time(best_start_time)}
        """
    else:
         return f"""
        {APOLOGY} Try saying something like this : 
        "Add a _____ hour long event to my calendar called _____ on _____.
        """


def list_events(args):
    service = build_google_api_service()
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
        {APOLOGY} Try saying: "What's on my calendar today?"
        """

# ------------------------
# NOT SUPPORTED YET 
# ------------------------
def get_event(eventId):
    return APOLOGY


def update_event(args):
    return APOLOGY


def delete_event(eventId):
      return APOLOGY








