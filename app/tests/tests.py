from dotenv import load_dotenv
from app.functions.openai.answer_question import answer_question
import os

load_dotenv()

# -------------------------------
# OPEN AI - GENERAL
# -------------------------------
def test_api_key_configuration():
    assert 'OPENAI_API_KEY' in os.environ, "API key not configured"


def test_openai_api_request():
    response = answer_question("Why is the sky blue?")
    assert response is not None, "Failed to receive response from OpenAI API"
    assert 'choices' in response, "Unexpected response format from OpenAI API"


def test_openai_api_rate_limit_handling():
    mock_rate_limit_error_response = {
        'error': 'Rate limit exceeded'
    }
    processed_rate_limit_error_response = app.process_openai_api_response(mock_rate_limit_error_response)
    assert processed_rate_limit_error_response is not None, "Failed to process rate limit error response"
    assert processed_rate_limit_error_response == "Error: Rate limit exceeded", "Unexpected rate limit error message"


# -------------------------------
# OPEN AI - FUNCTION CALLING
# -------------------------------
def test_openai_toolcalls_insert_event():
    pass

def test_openai_toolcalls_insert_event_while_avoiding_conflicts():
    pass

def test_openai_toolcalls_list_events():
    pass

def test_openai_toolcalls_delete_event():
    pass

def test_openai_toolcalls_update_event():
    pass


# -------------------------------
# GOOGLE CALENDAR
# -------------------------------
def test_insert_event():
    pass

def test_insert_event_while_avoiding_conflicts():
    pass

def test_list_events():
    pass

def test_delete_event():
    pass

def test_update_event():
    pass



# ----------------
# ERROR HANDLING
# ----------------
def test_openai_api_error_handling():
    # Mock error response from OpenAI API
    mock_error_response = {
        'error': 'Invalid request'
    }
    processed_error_response = app.process_openai_api_response(mock_error_response)
    assert processed_error_response is not None, "Failed to process OpenAI API error response"
    assert processed_error_response == "Error: Invalid request", "Unexpected error message"
