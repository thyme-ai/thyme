from app.functions.gcal.utils.execute_gcal_function_call import execute_gcal_function_call
from app.functions.openai.utils.pretty_print_conversation import pretty_print_conversation
from app.functions.openai.get_openai_prompt_header import get_openai_prompt_header
from app.functions.helpers import get_user_by_email, check_for_credentials
from app.functions.openai.utils.get_tools import get_tools
from flask import session
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

GPT_MODEL = "gpt-3.5-turbo"
APOLOGY_STRING = "Sorry, I'm not able to do that yet."
MAX_ATTEMPTS = 3
TOOLS = get_tools()

client = OpenAI()

def answer_question(prompt):
    creds = check_for_credentials()
    user = get_user_by_email(session['email'])
    openai_prompt_header = get_openai_prompt_header(user)
    messages = [{"content": openai_prompt_header, "role": "system"}, {"content": prompt, "role": "user"}]
    chat_response = chat_completion_request(messages, TOOLS)
    assistant_message = chat_response.choices[0].message

    # If the assistant added any relevant google calendar "tools" (i.e. functions) 
    # to the tool_calls property, execute the function 
    if assistant_message.tool_calls:
        assistant_message.content = str(assistant_message.tool_calls[0].function)
        messages.append({"role": assistant_message.role, "content": assistant_message.content})
        results = execute_gcal_function_call(assistant_message)

        # Add the results of the google calendar function call to the messages array 
        # so the user can see the results 
        messages.append({
            "role": "function", 
            "tool_call_id": assistant_message.tool_calls[0].id, 
            "name": assistant_message.tool_calls[0].function.name, 
            "content": results
            })
        
        # Pretty print the conversation in the terminal 
        pretty_print_conversation(messages)
        return results
    
    # Otherwise, just answer the user's question and don't call any google calendar functions
    else: 
        answer = chat_response.choices[0].message.content
        return answer
    

# If chat completion fails, it tries again MAX_ATTEMPTS more times and then stops 
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(MAX_ATTEMPTS))
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



