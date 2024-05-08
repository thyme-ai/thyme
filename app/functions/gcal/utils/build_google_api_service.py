from googleapiclient.discovery import build
from app.functions.gcal.helpers.user import get_credentials


# Builds a service object for the Google Python API client which allows you to easily use
# built-in methods to access API endpoints for a particular Google API  
# you can use the servvice objects to easily make calls to the API instead of having 
# to specify the endpoints yourself
def build_google_api_service():
    credentials = get_credentials()
    service = build("calendar", "v3", credentials=credentials)
    return service
