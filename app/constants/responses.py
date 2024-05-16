from app.constants.general import APOLOGY
from app.functions.gcal.helpers.datetime import get_easy_read_time

# -----------
# FAIL 
# -----------
CREATE_FAIL = f"""
    {APOLOGY} Try saying something like this : 
    "Add a _____ hour long event to my calendar called _____ on _____."""

CREATE_AND_AVOID_CONFLICTS_FAIL = f"""
    Sorry, I couldn't find any free times for your event within your 
    preferred wake up & sleep times. Try a different time or day."""

READ_FAIL = f"""{APOLOGY} Try saying: "What's on my calendar today?" """

READ_NO_EVENTS_FOUND = f"""There are no events on your calendar that day."""

# -----------
# SUCCESS 
# -----------
def get_create_sucess_message(event):
    return f"""
        I created your event called {event.get("summary")} 
        at {get_easy_read_time(event.get("start").get("dateTime"))}
    """


def get_create_and_avoid_conflicts_sucess_message(event):
    return f"""
        I created your event called {event.get("summary")}
        at the closest available time within your preferred wake & sleep hours 
        which was {get_easy_read_time(event.get("start").get("dateTime"))}
    """



