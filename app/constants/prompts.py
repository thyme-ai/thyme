# Example Event 
SUMMARY = "Brainstorm"
DURATION = "2 hours"
DAY = "today"
TIME = "1 pm"
EVENT = ["an event", "a meeting", "a block", "a meeting block"]
CREATE = ["create", "add", "book", "insert", "schedule"]

# With/Without Time Specified
WITH_DATE_AND_TIME = f"called {SUMMARY} for {DURATION} at {TIME} {DAY}"
WITH_DATE = f"called {SUMMARY} for {DURATION} {DAY}"

# Weekdays
RELATIVE_WORDS = ["this", "next", "last"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# TODO - add function for dateutil parser to interpret these, for now, we rely on the LLM to convert these words to datetimes 
# RECENT_DAYS = ["Today", "Tomorrow", "Yesterday"] 

# Meeting Conflict Avoidance
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

# ------------
# HELPERS
# ------------
def get_prompt_variants(verbs, nouns, middle=' ', tail=' '):
    result = []
    for i in range(len(verbs)):
        for j in range(len(nouns)):
            result.append(f"{verbs[i]}{middle}{nouns[j]} {tail}")
    return result

def get_variants_of_non_numeric_date_strings():
    RELATIVE_WEEKDAYS = get_prompt_variants(verbs=RELATIVE_WORDS, nouns=WEEKDAYS)
    return [*WEEKDAYS, *RELATIVE_WEEKDAYS]

# For Interpreting Date Strings in User's Prompt
NON_NUMERIC_DATE_STRINGS = get_variants_of_non_numeric_date_strings()


# ----------------
# PROMPT VARIANTS
# ----------------
def get_variants_of_create_event_with_date_only():
    return get_prompt_variants(verbs=CREATE, nouns=EVENT, tail=WITH_DATE)


def get_variants_of_create_event_with_date_and_time():
    return get_prompt_variants(verbs=['Add'], nouns=['event'], tail=WITH_DATE_AND_TIME)


def get_variants_of_create_event_while_avoiding_conflicts():
    create_events = [f'Add an event {WITH_DATE}'] 
    avoid_after = get_prompt_variants(verbs=create_events, nouns=AVOID_AFTER, middle=' and ')
    avoid_before = get_prompt_variants(verbs=AVOID_BEFORE, nouns=['event'], tail=WITH_DATE)
    return [*create_events, *avoid_after, *avoid_before]


def get_variants_of_read_events():
    return get_prompt_variants(verbs=GET_EVENTS, nouns=NON_NUMERIC_DATE_STRINGS)


# Prompt Variants to be provided to LLM to help determine when to call functions
VARIANTS_CREATE_EVENT = get_variants_of_create_event_with_date_and_time() 
VARIANTS_CREATE_EVENT_WITH_CONFLICT_AVOIDANCE = get_variants_of_create_event_while_avoiding_conflicts()
VARIANTS_READ_EVENTS = get_variants_of_read_events()
