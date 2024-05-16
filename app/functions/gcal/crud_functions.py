from app.constants.general import APOLOGY, CALENDAR_ID
from app.constants.responses import (
    CREATE_FAIL, 
    CREATE_AND_AVOID_CONFLICTS_FAIL, 
    READ_NO_EVENTS_FOUND, 
    get_create_sucess_message, 
    get_create_and_avoid_conflicts_sucess_message
)
from app.functions.gcal.utils.build_google_api_service import build_google_api_service
from app.functions.gcal.helpers.datetime import get_datetime_string, get_datetime_object
from app.functions.thyme.helpers.conflict_avoidance import (
    get_suggested_start_time, 
    get_busy_ranges_within_awake_range, 
    get_awake_range
)
from app.functions.gcal.helpers.datetime import get_easy_read_time


def insert_event(args):
    service = build_google_api_service()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()
    if event:
        return get_create_sucess_message(event)
    else:
         return CREATE_FAIL


def insert_event_while_avoiding_conflicts(args):
    ideal_start = get_datetime_object(args['start']['dateTime'])
    ideal_end = get_datetime_object(args['end']['dateTime'])
    duration = ideal_end - ideal_start

    # Get suggested start time for event, within user's awake hours & without conflicts
    busy_ranges = get_busy_ranges_within_awake_range(ideal_start)
    awake_range = get_awake_range(ideal_start)
    suggested_start = get_suggested_start_time(ideal_start, ideal_end, awake_range, busy_ranges)
    if not suggested_start:
        return CREATE_AND_AVOID_CONFLICTS_FAIL
    
    # Create event in User's Google Calendar
    args['start']['dateTime'] = get_datetime_string(suggested_start)
    args['end']['dateTime'] = get_datetime_string(suggested_start + duration)
    service = build_google_api_service()
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()

    if event:
        return get_create_and_avoid_conflicts_sucess_message(event)
    else:
         return CREATE_AND_AVOID_CONFLICTS_FAIL


def list_events(args):
    service = build_google_api_service()
    params = {"calendarId": CALENDAR_ID, "showDeleted": False, "singleEvents": True}
    
    for key in args.keys():
        params[key] = args.get(key)
    events = service.events().list(**params).execute()['items']

    print('EVENTS', events)

    if events:
        event_strings = []
        for event in events: 
            if event['status'] != 'cancelled':
                event_strings.append(f"{event['summary']} at { get_easy_read_time(event['start']['dateTime']) }")
        
        return f"Here are the events on your calendar: {(", ").join(event_strings)}"
    return READ_NO_EVENTS_FOUND


# ------------------------
# NOT SUPPORTED YET 
# ------------------------
def get_event(eventId):
    return APOLOGY


def update_event(args):
    return APOLOGY


def delete_event(eventId):
      return APOLOGY