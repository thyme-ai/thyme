from app.models import User
from app.functions.openai.utils.get_tools import get_tools
from app.functions.openai.utils.get_openai_prompt_header import get_openai_prompt_header
from datetime import time

GPT_MODEL = "gpt-3.5-turbo"
MAX_ATTEMPTS = 3
MAX_WAIT = 40
TOOLS = get_tools()

# --------------
# RESPONSES
# ---------------
APOLOGY = "Sorry, I'm not able to do that yet."

# --------------
# TESTING
# ---------------
USER = User(
       email = "hello@thyme.company",
       timezone = "America/Los_Angeles",
       wake_time = time(hour=7, minute=0),
       sleep_time = time(hour=22, minute=0),
       )
SUMMARY = "Brainstorm"
DURATION = "2 hours"
DAY = "today"
TIME = "1 pm"
PROMPT_HEADER = get_openai_prompt_header(USER)

CREATE_VARIANTS = [ "create", "add", "book", "set", "schedule"]