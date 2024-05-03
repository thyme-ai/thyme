from app.functions.google_calendar_api.gcal_functions import (
    insert_event, get_event, list_events, update_event, delete_event, get_busy_times
)
from app.functions.helpers import check_for_credentials
import json


function_name_to_function = {
   "insert_event": insert_event,
   "list_events": list_events,
   "get_busy_times": get_busy_times,
#    "delete_event": delete_event,
#    "get_event": get_event,
#    "update_event": update_event
}


def execute_gcal_function_call(message):
    function_name = message.tool_calls[0].function.name
    args_json = message.tool_calls[0].function.arguments
    args = None

    if function_name == 'insert_event':
        args = json.loads(args_json).get('requestBody')

    if function_name == 'list_events':
        args = json.loads(args_json).get('parameters')

    if function_name == 'get_busy_times':
        print('ARGS FOR GET BUSY TIMES-------', args_json)
        args = json.loads(args_json).get('day')

    # -----------------------------------------------------------------
    # TODO - add cases for "get_event", "delete_event", "update_event"
    # -----------------------------------------------------------------
    
    crud_function = function_name_to_function.get(function_name)
    return crud_function(args)