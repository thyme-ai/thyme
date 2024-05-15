from app.constants.testing import SUMMARY, DURATION, TIME, DAY

WITH_DATE_AND_TIME = f"called {SUMMARY} for {DURATION} at {TIME} {DAY}"
WITH_DATE = f"called {SUMMARY} for {DURATION} {DAY}"

# --------------------------------------------------------------------------------
# Uncomment the shorter versions of EVENT & CREATE to run new tests more quickly
# --------------------------------------------------------------------------------
EVENT = ["an event"]
CREATE = ["Create"]
# EVENT = ["an event", "a meeting", "a block", "a meeting block"]
# CREATE = ["create", "add", "book", "insert", "schedule"]

SOME_DAY = ["today", "tomorrow", "Tuesday", "this Tuesday", "on the 15th"]
# ----------------------------------------------------

AVOID_AFTER = [
    "avoid conflicts",
    "avoid existing events",
    "don't schedule over other events"
]

AVOID_BEFORE = [
    "Find an open time for",
    "Find the best time for",
    "Find an available time for",
    "Find some time on my calendar for"
]

GET_EVENTS = [
    "What's on my calendar",
    "What meetings are on my calendar",
    "What do I have scheduled",
    "What do I have going on",
]


def get_variants_of_create_event_with_date_only():
    return get_prompt_variants(verbs=CREATE, nouns=EVENT, tail=WITH_DATE)

def get_variants_of_create_event_with_date_and_time():
    return get_prompt_variants(verbs=CREATE, nouns=EVENT, tail=WITH_DATE_AND_TIME)

def get_variants_of_create_event_while_avoiding_conflicts():
    create_events = get_variants_of_create_event_with_date_only()  
    avoid_after = get_prompt_variants(verbs=create_events, nouns=AVOID_AFTER, middle=' and ')
    avoid_before = get_prompt_variants(verbs=AVOID_BEFORE, nouns=EVENT, tail=WITH_DATE)
    return [*create_events, *avoid_after, *avoid_before]

def get_variants_of_read_events():
    return get_prompt_variants(verbs=GET_EVENTS, nouns=SOME_DAY)


# ------------
# HELPERS
# ------------
def get_prompt_variants(verbs, nouns, middle=' ', tail=' '):
    result = []
    for i in range(len(verbs)):
        for j in range(len(nouns)):
            result.append(f"{verbs[i]}{middle}{nouns[j]} {tail}")
    return result