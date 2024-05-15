from app.constants.general import GPT_MODEL, MAX_ATTEMPTS, MAX_WAIT, TOOLS
from app.functions.gcal.utils.execute_gcal_function import execute_gcal_function
from app.functions.openai.utils.pretty_print_chat import pretty_print_chat
from app.functions.openai.utils.get_openai_prompt_header import get_openai_prompt_header
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

client = OpenAI()

def answer_question(prompt, user):
    openai_prompt_header = get_openai_prompt_header(user)
    messages = [{"content": openai_prompt_header, "role": "system"}, {"content": prompt, "role": "user"}]
    chat_response = chat_completion_request(messages, TOOLS)
    assistant_message = chat_response.choices[0].message

    # If assistant found any relevant Google Calendar "tools" (i.e. functions), execute them
    if assistant_message.tool_calls:
        assistant_message.content = str(assistant_message.tool_calls[0].function)

        # Add the function call to the messages array
        messages.append({
            "role": assistant_message.role, 
            "content": None,
            "function_name": assistant_message.tool_calls[0].function.name, 
            "function_call": assistant_message.tool_calls[0].function.arguments
            })
        
        # Execute the function
        result = execute_gcal_function(assistant_message)

        # Add the result of the function call to the messages array 
        messages.append({
            "role": "function", 
            "function_name": assistant_message.tool_calls[0].function.name, 
            "content": result
            })
            
    # Otherwise, just answer the user's question
    else: 
        result = chat_response.choices[0].message.content
        messages.append({
            "role": "assistant", 
            "content": result
        })
    
    pretty_print_chat(messages)
    return messages
    

# If chat completion fails, wait MAX_WAIT seconds & try again MAX_ATTEMPTS more times
@retry(wait=wait_random_exponential(multiplier=1, max=MAX_WAIT), stop=stop_after_attempt(MAX_ATTEMPTS))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as error:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {error}")
        return error



