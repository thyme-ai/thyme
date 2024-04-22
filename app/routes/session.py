from flask import Blueprint, redirect, url_for, render_template
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os.path

bp = Blueprint("session", __name__, url_prefix="/session")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

@bp.route("/login", methods=["GET", "POST"])
def login():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available or they expired, let the user log in.
    if not creds or not creds.valid:
      # If the credentials have expired, also let the user log in 
      if creds and creds.expired and creds.refresh_token:
        creds.refresh()
      # else, get user credentials 
      else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

      return redirect(url_for("home.assistant"))
    

@bp.route("/logout", methods=["GET", "POST"])
def logout():
  # Get the path to the token.json file
  token_file_path = os.path.join(os.getcwd(), "token.json")

  # Check if the file exists
  if os.path.exists(token_file_path):
      # Delete the file
      os.remove(token_file_path)
      print("The token.json file has been removed.")
  else:
      print("The token.json file does not exist.")

  return redirect(url_for("home.index"))