from dotenv import load_dotenv
from app.functions.openai.answer_question import chat_completion_request
import os
import pytest

load_dotenv()

@pytest.mark.skip
def test_api_key_configuration():
    assert 'OPENAI_API_KEY' in os.environ, "API key not configured"

@pytest.mark.skip
def test_openai_api_request():
    prompt = "Why is the sky blue?"
    messages = [{"content": prompt, "role": "user"}]
    response = chat_completion_request(messages)
    assert response is not None, "Failed to receive response from OpenAI API"

@pytest.mark.skip
def test_openai_api_error_handling():
    mock_rate_limit_error_response = "'error': 'Rate limit exceeded'"
    messages = [{"content": mock_rate_limit_error_response, "role": "assistant"}]
    processed_rate_limit_error_response = chat_completion_request(messages)
    assert processed_rate_limit_error_response is not None, "Failed to process rate limit error response"