from app.functions.openai.answer_question import answer_question
from app.constants.testing import USER_FOR_TESTING
import pytest 

@pytest.mark.skip
def test_answer_question():
    prompt = "Why is the sky blue?"
    response = answer_question(prompt, USER_FOR_TESTING)
    assert response is not None, "answer_question function did not give a response"


@pytest.mark.skip
def test_answer_question_long():
    prompt = "Tell me 10 facts about Whale Sharks"
    response = answer_question(prompt, USER_FOR_TESTING)
    assert response is not None, "answer_question function did not give a response"