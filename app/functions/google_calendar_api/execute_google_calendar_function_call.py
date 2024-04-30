from googleapiclient.discovery import build
import json
from app.functions.google_calendar_api.google_calendar_event_crud_operations import (
    insert_event, get_event, list_events, update_event, delete_event)

function_name_to_function = {
   "insert_event": insert_event,
   "delete_event": delete_event,
   "get_event": get_event,
   "list_events": list_events,
   "update_event": update_event
}

def execute_google_calendar_function_call(message, creds):
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