from app.functions.openai.answer_question import chat_completion_request
from pytest import mark
from app.constants import SUMMARY, DURATION, TIME, DAY, TOOLS, PROMPT_HEADER
from app.constants import CREATE_VARIANTS

@mark.parametrize("create_variant", [*CREATE_VARIANTS])
def test_create_event(create_variant):
    prompt = f"""
    {create_variant} an event to my calendar called {SUMMARY} 
    for {DURATION} at {TIME} {DAY}"""
    messages = [{"content": PROMPT_HEADER, "role": "system"}, {"content": prompt, "role": "user"}]
    result = chat_completion_request(messages=messages, tools=TOOLS)
    assert result != None
    assert 'insert_event' in str(result)