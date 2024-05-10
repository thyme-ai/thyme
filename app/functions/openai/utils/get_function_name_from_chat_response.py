def get_function_name_from_chat_response(response):
    return response.choices[0].message.tool_calls[0].function.name