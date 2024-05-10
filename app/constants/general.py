from app.functions.openai.utils.get_tools import get_tools
from datetime import timedelta
from os import environ
from dotenv import load_dotenv
import json 

load_dotenv()

# ---------
# OPEN AI
# ---------
GPT_MODEL = "gpt-3.5-turbo"
MAX_ATTEMPTS = 3
MAX_WAIT = 40

# -------
# GOOGLE 
# -------
GOOGLE_CLIENT_CONFIG = json.loads(environ.get('GOOGLE_CLIENT_CONFIG'))
CALENDAR_ID = 'primary'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",  # edit events in all your calendars (you cant edit/share/delete calendars)
    "https://www.googleapis.com/auth/userinfo.email",   # get user's email address
    "https://www.googleapis.com/auth/userinfo.profile", # get user's email address
    "https://www.googleapis.com/auth/calendar.readonly" # get calendar settings (including)
]



# ---------
# THYME 
# ---------
APOLOGY = "Sorry, I'm not able to do that yet."
DEFAULT_EVENT_DURATION = "1 hour"
MAX_DELTA = timedelta(minutes=12*60) # when suggesting available times for events 
INCREMENT = timedelta(minutes=30)    # when suggesting available times for events 
TOOLS = get_tools()                  # 'tools' (i.e. functions) that Open AI can use to create arguments for function calls