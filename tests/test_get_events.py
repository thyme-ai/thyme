from app.functions.openai.answer_question import chat_completion_request
from pytest import mark
from app.constants.general import TOOLS 
from app.constants.testing import USER_FOR_TESTING
from app.constants.prompts import get_variants_of_read_events
from app.functions.openai.utils.get_function_name_from_chat_response import get_function_name_from_chat_response
from app.functions.openai.utils.get_openai_prompt_header import get_openai_prompt_header

# @pytest.mark.skip
@mark.parametrize("variant", [*get_variants_of_read_events()])
def test_get_event(variant):
    PROMPT_HEADER_FOR_TESTING = get_openai_prompt_header(USER_FOR_TESTING)
    messages = [
        {"content": PROMPT_HEADER_FOR_TESTING, "role": "system"}, 
        {"content": variant, "role": "user"}
    ]
    result = chat_completion_request(messages=messages, tools=TOOLS)
    function_name = get_function_name_from_chat_response(result)
    print(variant)
    assert function_name == 'list_events'

