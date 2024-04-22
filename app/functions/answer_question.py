from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from app.functions.get_gcal_functions_from_openai_spec import get_gcal_functions_from_openai_spec
from app.functions.pretty_print_conversation import pretty_print_conversation

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = 'primary'
GPT_MODEL = "gpt-3.5-turbo"
TOOLS = get_gcal_functions_from_openai_spec()
PST_HOURS_FROM_UTC = -7
timezone_pst = timezone(timedelta(hours=PST_HOURS_FROM_UTC))
now = datetime.now(timezone_pst)

system_message = f"""
You are a helpful assistant. 

Assume that today is {now} and that the timezone is {timezone_pst}

Respond to the following prompt.
If the prompt does not contain calendar-related tasks, just respond normally
and format the text so that it is easy to read. 

If the prompt contains calendar-related tasks, respond to the following prompt
by using function_call and then summarize actions. 

If you are making a call to the "create_event" function, make the event summary 
start with an emogee that describes the event.

If the prompt contains a request for ideas or suggestions, 
add your suggestions to the description of the event as a numbered list.

Ask for clarification if a user request is ambiguous.
"""

client = OpenAI()

def answer_question(prompt, creds):
    messages = [{"content": system_message, "role": "system"}, {"content": prompt, "role": "user"}]
    chat_response = chat_completion_request(messages, TOOLS)
    assistant_message = chat_response.choices[0].message

    # If there is a relevant Google Calendar CRUD Operation 
    if assistant_message.tool_calls:
        assistant_message.content = str(assistant_message.tool_calls[0].function)
        messages.append({"role": assistant_message.role, "content": assistant_message.content})
        results = execute_function_call(assistant_message, creds)
        messages.append({
            "role": "function", 
            "tool_call_id": assistant_message.tool_calls[0].id, 
            "name": assistant_message.tool_calls[0].function.name, 
            "content": results
            })
        pretty_print_conversation(messages)
        return results
    # Otherwise, just answer the question and don't call any functions
    else: 
        answer = chat_response.choices[0].message.content
        return answer
    

# ---------------
# HELPERS
# ---------------
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def execute_function_call(message, creds):
    service = build("calendar", "v3", credentials=creds)
    function_name = message.tool_calls[0].function.name
    args_json = message.tool_calls[0].function.arguments
    args = None

    if function_name == 'insert_event':
        args = json.loads(args_json).get('requestBody')

    if function_name == 'list_events':
        args = json.loads(args_json).get('parameters')

    # if function_name == 'get_event':
    #     args = json.loads(args_json).get('parameters')

    # if function_name == 'delete_event':
    #     args = json.loads(args_json).get('parameters')
    

    crud_function = function_name_to_function.get(function_name)
    return crud_function(service, args)

# ----------------
# CRUD OPERATIONS
# ----------------
def insert_event(service, args):
    event = service.events().insert(calendarId=CALENDAR_ID, body=args).execute()
    return f"I created your event called {event.get("summary")}. Find it here - {event.get("htmlLink")} "


def list_events(service, args):
    params = {"calendarId": "primary"}
    for key in args.keys():
        params[key] = args.get(key)
    events = service.events().list(**params).execute()['items']
    event_summaries = (", ").join(map(lambda e: f"{e.get('summary')}", events))
    return event_summaries

def delete_event(service, eventId):
#    event = get_event(service, eventId)
#    service.events().delete(calendarId='primary', eventId=eventId).execute()
#    return f"I deleted your event called {event['summary']}"
    pass


def get_event(service, eventId):
    # event = service.events().get(calendarId='primary', eventId=eventId).execute()
    # return f"{event['summary']}"
    pass


def update_event(service, args):
   pass


function_name_to_function = {
   "insert_event": insert_event,
   "delete_event": delete_event,
   "get_event": get_event,
   "list_events": list_events,
   "update_event": update_event
}