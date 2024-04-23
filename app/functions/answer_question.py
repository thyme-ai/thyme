from googleapiclient.discovery import build
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from app.functions.get_gcal_functions_from_openai_spec import get_gcal_functions_from_openai_spec
from app.functions.pretty_print_conversation import pretty_print_conversation
from app.api_specs.openai_api.openai_prompt import openai_prompt
import datetime 
from datetime import datetime 

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = 'primary'
GPT_MODEL = "gpt-3.5-turbo"
TOOLS = get_gcal_functions_from_openai_spec()
APOLOGY_STRING = "Sorry, I'm not able to do that yet."

system_message = openai_prompt

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

    if event:
        return f"I created your event called {event.get("summary")}"
    else:
         return f"""
        {APOLOGY_STRING} Try saying something like this : 
        "Add an event to my calendar called *name of event* on *date* at *time* for *duration*
         that repeats *frequency of repeats*
        """


def list_events(service, args):
    params = {"calendarId": "primary"}
    for key in args.keys():
        params[key] = args.get(key)
    events = service.events().list(**params).execute()['items']

    if events:
        print('EVENTS', events)
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
        "Give me a list of events on my calendar called..."
        """

def delete_event(service, eventId):
      return APOLOGY_STRING


def get_event(service, eventId):
    return APOLOGY_STRING


def update_event(service, args):
    return APOLOGY_STRING


function_name_to_function = {
   "insert_event": insert_event,
   "delete_event": delete_event,
   "get_event": get_event,
   "list_events": list_events,
   "update_event": update_event
}