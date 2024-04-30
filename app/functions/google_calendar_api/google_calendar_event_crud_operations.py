from datetime import datetime 

CALENDAR_ID = 'primary'
APOLOGY_STRING = "Sorry, I'm not able to do that yet."

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

