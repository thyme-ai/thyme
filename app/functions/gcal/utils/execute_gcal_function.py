from app.constants.general import APOLOGY
from app.functions.gcal.crud_functions import insert_event, list_events, insert_event_while_avoiding_conflicts
import json

function_name_to_function = {
   "insert_event": insert_event,
   "insert_event_while_avoiding_conflicts": insert_event_while_avoiding_conflicts,
    "list_events": list_events,

}


def execute_gcal_function(message):
    function_name = message.tool_calls[0].function.name
    args_json = message.tool_calls[0].function.arguments
    args = None

    if function_name == 'insert_event' or function_name == 'insert_event_while_avoiding_conflicts':
        args = json.loads(args_json).get('requestBody')

    if function_name == 'list_events':
        args = json.loads(args_json).get('parameters')
    
    if function_name and args:
        crud_function = function_name_to_function.get(function_name)
        return crud_function(args)
    
    return APOLOGY