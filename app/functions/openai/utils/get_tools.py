import jsonref

# Creats an array of "tools" that will be passed to the OpenAI API so that 
# it can suggest function_calls in its chat responses
# Read more about calling functions with chat models here - 
# https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
def get_tools():
    # -----------------
    # CUSTOM FUNCTIONS
    # -----------------
    with open('./app/specs/custom/get_busy_times_function_spec.json', 'r') as f:
        get_busy_times_function_spec = jsonref.loads(f.read()) 

    custom_functions = [get_busy_times_function_spec]


    # --------------------
    # BUILT-IN FUNCTIONS
    # --------------------
    # Get Open API formatted spec for Google Calendar API (created with the help of Chat GPT)
    with open('./app/specs/gcal/google_calendar_api_spec.json', 'r') as f:
        openapi_spec_for_gcal = jsonref.loads(f.read()) 

    functions = []

    # Convert Open API Spec into functions (this code is from the Open AI Cookbook)
    for path, methods in openapi_spec_for_gcal["paths"].items():
        for method, spec_with_ref in methods.items():
            # 1. Resolve JSON references.
            spec = jsonref.replace_refs(spec_with_ref)

            # 2. Extract a name for the functions.
            function_name = spec.get("operationId")

            # 3. Extract a description and parameters.
            desc = spec.get("description") or spec.get("summary", "")

            schema = {"type": "object", "properties": {}}

            req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if req_body:
                schema["properties"]["requestBody"] = req_body

            params = spec.get("parameters", [])
            if params:
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                schema["properties"]["parameters"] = {
                    "type": "object",
                    "properties": param_properties,
                }

            functions.append(
                {"type": "function", "function": {"name": function_name, "description": desc, "parameters": schema}}
            )

    return [*functions, *custom_functions]

