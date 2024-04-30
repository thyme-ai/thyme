from datetime import datetime, timezone, timedelta
from app.functions.google_calendar_api.get_hours_from_utc_from_timezone_name import get_hours_from_utc_from_timezone_name

def get_openai_prompt_header(user):
    timezone_name = user.timezone
    hours_from_utc = get_hours_from_utc_from_timezone_name(timezone_name)
    timezone_user = timezone(timedelta(hours=hours_from_utc))
    now = datetime.now(timezone_user)

    header = f"""
    You are a helpful assistant. 

    Assume that today is {now} and that the timezone is {timezone_user}

    Respond to the following prompt.
    If the prompt does not contain calendar-related tasks, just respond normally
    and format the text so that it is easy to read. 

    If the prompt contains calendar-related tasks, respond to the following prompt
    by using function_call and then summarize actions. 

    If you are making a call to the "insert_event" function, make the event summary 
    start with an emogee that describes the event.

    If the prompt contains a request for ideas or suggestions, 
    add your suggestions to the description of the event as a numbered list.

    Ask for clarification if a user request is ambiguous.
    """

    return header