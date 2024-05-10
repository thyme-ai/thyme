from app.constants.testing import SUMMARY, DURATION, TIME, DAY

WITH_DATE_AND_TIME = f"called {SUMMARY} for {DURATION} at {TIME} {DAY}"
WITH_DATE = f"called {SUMMARY} for {DURATION} {DAY}"

EVENT = ["an event", "a meeting", "a block", "a meeting block"]
CREATE = ["create", "add", "book", "insert", "schedule"]

# Short Version for Testings New Test Cases Quickly
# EVENT = ["an event"]
# CREATE = ["Create"]

AVOID_AFTER = [
    "avoid conflicts",
    "avoid existing events",
    "don't schedule over other events"
]
AVOID_BEFORE = [
    "Find an open time for",
    "Find the best time for",
    "Find an available time for",
]


def get_variants_of_create_event_with_date_only():
    result = []
    for e in range(len(EVENT)):
        for c in range(len(CREATE)):
            result.append(f"{CREATE[c]} {EVENT[e]} {WITH_DATE}")
    return result


def get_variants_of_create_event_with_date_and_time():
    result = []
    for e in range(len(EVENT)):
        for c in range(len(CREATE)):
            result.append(f"{CREATE[c]} {EVENT[e]} {WITH_DATE_AND_TIME}")
    return result


def get_variants_of_create_event_while_avoiding_conflicts():
    create_events = get_variants_of_create_event_with_date_only()  
    result = []

    for c in range(len(create_events)):
        for a in range(len(AVOID_AFTER)):
            result.append(f"{create_events[c]} and {AVOID_AFTER[a]}")

        for b in range(len(AVOID_BEFORE)):
            result.append(f"{AVOID_BEFORE[b]} an event {WITH_DATE} ")
    return result
    