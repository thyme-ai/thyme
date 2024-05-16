from app.functions.openai.answer_question import chat_completion_request
from pytest import mark
from app.constants.general import TOOLS 
from app.constants.testing import USER_FOR_TESTING
from app.constants.prompts import VARIANTS_READ_EVENTS
from app.functions.openai.utils.get_function_name_from_chat_response import get_function_name_from_chat_response
from app.functions.openai.utils.get_openai_prompt_header import get_openai_prompt_header
import pytest


# --------------------------------------------
# Uncomment the following for Quick Testing
# --------------------------------------------
VARIANTS_READ_EVENTS = VARIANTS_READ_EVENTS[0:2]
# --------------------------------------------

# @pytest.mark.skip
@mark.parametrize("variant", [*VARIANTS_READ_EVENTS])
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

