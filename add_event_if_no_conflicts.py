# ------------------------------------------------
# The following code was written by Yousef Nami,
# except where it says "added by fwesparza"
# Thank you Yousef!
# ------------------------------------------------
# - Github - https://github.com/namiyousef
# - LinkedIn - https://www.linkedin.com/in/namiyousef96/?originalSubdomain=uk
# - Medium - https://medium.com/p/be27c1600e7e

import logging
import os
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# -- In the actual code, I have these imported from config.py
# GOOGLE_OAUTH_CREDENTIAL_FILE = os.environ.get(
#     "GOOGLE_OAUTH_CREDENTIAL_FILE", "google_oauth_credentials.json"
# )

# GOOGLE_OAUTH_TOKEN = os.environ.get(
#     "GOOGLE_OAUTH_TOKEN", "google_oauth_token.json"
# )

GOOGLE_OAUTH_TOKEN = "token.json"
GOOGLE_OAUTH_CREDENTIAL_FILE = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar",         # edit calendar
    # "https://www.googleapis.com/auth/userinfo.email",   # get email 
    # "https://www.googleapis.com/auth/calendar.readonly" # get timezone
]

# ------------------------------------------------------------------------
# -- In the actual code, I have these imported from a data or types file
from enum import Enum
from typing import Dict
class ConflictResolutionStrategy(str, Enum):
    FAIL = "fail"
    REPLACE = "replace"
    IGNORE = "ignore"
    APPEND = "append"

APIResponse = Dict[str, int | str | list]
# -----------------------------------------------------------------------

# -- define logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- define scopes
# SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarClient:
    def __init__(
        self,
    ):
        self.client = self.initialise()

    def initialise(
        self,
    ):
        credentials = None
        if os.path.exists(GOOGLE_OAUTH_TOKEN):
            logger.info("Detected google oauth token... validating...")
            credentials = Credentials.from_authorized_user_file(
                GOOGLE_OAUTH_TOKEN, SCOPES
            )
            if credentials.expired and credentials.refresh_token:
                logger.info("Credentials have expired... refreshing...")
                credentials.refresh(Request())
                with open(GOOGLE_OAUTH_TOKEN, "w") as f:
                    f.write(credentials.to_json())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_OAUTH_CREDENTIAL_FILE, SCOPES
                )
            except FileNotFoundError as file_not_found_error:
                raise ConnectionError(
                    f"Could not find Google OAuth Credentals file: `{GOOGLE_OAUTH_CREDENTIAL_FILE}`"
                ) from file_not_found_error

            logger.info("Running flow...")
            credentials = flow.run_local_server()
            with open(GOOGLE_OAUTH_TOKEN, "w") as f:
                f.write(credentials.to_json())

        logger.info("Initialising client...")
        client = build("calendar", "v3", credentials=credentials)

        return client

    def _get_calendars(self):
        logger.info("Getting list of calendar available...")
        calendars = self.client.calendarList().list().execute()["items"]
        logger.debug(f"Got {len(calendars)} calendars")
        print('CALENDARS FOUND', calendars)
        return calendars

    def _generate_events_conflict_metadata(self, event_conflict_identifiers):
        # ---------------------
        # Added by fwesparza: 
        # CONFLICT_PROPERTIES_MAP maps properties of an Event Resource to arguments of a .list query 
        # See documentation for each 
        # - Event Resources - https://developers.google.com/calendar/api/v3/reference/events
        # - Event.list (get a list of Events that match the requirements) - https://developers.google.com/calendar/api/v3/reference/events/list
        # ---------------------
        CONFLICT_PROPERTIES_MAP = {
            "summary": lambda x: ("q", x),
            "iCalUID": lambda x: ("iCalUID", x),
            "start": lambda x: ("timeMax", x), # added be fwesparza
        }

        conflict_metadata = {}
        for (
            conflict_property,
            conflict_value,
        ) in event_conflict_identifiers.items():
            conflict_query_generator = CONFLICT_PROPERTIES_MAP.get(
                conflict_property
            )
            if conflict_query_generator is None:
                raise NotImplementedError(
                    f"Tried to find conflicts using calendar metadata `{conflict_property}` but there is currently no support for this"
                )

            key, value = conflict_query_generator(conflict_value)
            if key in conflict_metadata:
                raise Exception("not expected")

            conflict_metadata[key] = value

        return conflict_metadata

    def create_events(
        self,
        calendar_id: str,
        events: list,
        on_asset_conflict: str = "append",
        on_data_conflict: str = "fail",
        data_conflict_properties: list | None = None,
        create_calendar_if_not_exist: bool = False,
    ) -> APIResponse:
        """Function to add events to a calendar

        :param calendar_id: id of the calendar. See calendar resource for more information: https://developers.google.com/calendar/api/v3/reference/calendars
        :param events: events to create. See for more information: https://developers.google.com/calendar/api/v3/reference/events/insert
        :param on_asset_conflict: specify behaviour if calendar_id already exists, defaults to "ignore"
        :param on_data_conflict: specify behaviour if event already exists, defaults to "ignore"
        :param data_conflict_properties: event properties to check for conflicts, defaults to None
        :param create_calendar_if_not_exist: flag to create a calendar if it does not already exist, defaults to False
        """
        try:
            calendars = self._get_calendars()
        except HttpError as http_error:
            return {
                "status_code": http_error.status_code,
                "msg": f"Could not read calendar information. Reason: {http_error}",
            }

        _calendars_available = {calendar["id"] for calendar in calendars}
        if calendar_id not in _calendars_available:
            logger.info(
                f"calendar with calendar_id=`{calendar_id}` does not exist"
            )
            if create_calendar_if_not_exist:
                logger.info(f"Creating new calendar=`{calendar_id}`...")
                raise NotImplementedError(
                    (
                        f"Could not find calendar with calendar_id=`{calendar_id}`. At the moment "
                        "there is no support for creating new calendars from "
                        "the client. Please do this manually on the web and "
                        "try again."
                    )
                )
            else:
                return {
                    "status_code": 404,
                    "msg": f"Could not find calendar with calendar_id=`{calendar_id}`. If you wish to "
                    "create it, set table creation to `True`",
                }
        else:
            logger.info(
                f"Calendar with calendar_id=`{calendar_id}` exists... checking for conflicts..."
            )
            match on_asset_conflict:
                case ConflictResolutionStrategy.FAIL:
                    _msg = f"calendar with calendar_id=`{calendar_id}` exists and on_asset_conflict=`{on_asset_conflict}`. If you wish to edit calendar please change conflict_resolution_strategy"
                    logger.error(_msg)
                    return {
                        "status_code": 409,
                        "msg": _msg,
                    }
                case ConflictResolutionStrategy.IGNORE:
                    _msg = (
                        f"calendar_id=`{calendar_id}` exists but request dropped since "
                        "on_asset_conflict=`ignore`"
                    )
                    logger.info(_msg)
                    return {"status_code": 200, "msg": _msg}
                case ConflictResolutionStrategy.REPLACE:
                    _msg = f"calendar with calendar_id=`{calendar_id}` exists and on_asset_conflict=`{on_asset_conflict}`. There is currently no support for this."
                    logger.error(_msg)
                    raise NotImplementedError(_msg)
                case _:
                    logger.info(
                        "on_asset_conflict set to `append`... ignoring any conflicts..."
                    )

        if on_data_conflict == ConflictResolutionStrategy.REPLACE:
            raise NotImplementedError("No support for this yet")

        events_session = self.client.events()

        events_to_create = dict(enumerate(events))
        num_events_to_create = len(events_to_create)
        logger.info(f"Got {num_events_to_create} events to write")

        if on_data_conflict != ConflictResolutionStrategy.APPEND:
            logger.info(f"Checking {num_events_to_create} for conflicts...")
            conflict_events = []
            for event_count, event_id in enumerate(
                list(events_to_create.keys())
            ):
                logger.debug(
                    f"Checking event {event_count+1}/{num_events_to_create}..."
                )
                event = events_to_create[event_id]
                if data_conflict_properties is None:
                    _data_conflict_properties = list(event.keys())
                else:
                    _data_conflict_properties = data_conflict_properties

                event_conflict_identifiers = {
                    conflict_property: event[conflict_property]
                    for conflict_property in _data_conflict_properties
                }
                conflict_metadata = self._generate_events_conflict_metadata(
                    event_conflict_identifiers
                )
                logger.debug(
                    f"Searching calendar_id=`{calendar_id}` for events with the following properties: {_data_conflict_properties}"
                )
                try:
                    event_list = events_session.list(
                        calendarId=calendar_id, **conflict_metadata
                    ).execute()
                except HttpError as http_error:
                    raise Exception(
                        f"There was a failure in looking for conflicts for event_id=`{event_id}`. Reason: {http_error}"
                    ) from http_error

                conflicting_events = event_list["items"]
                num_conflicting_events = len(conflicting_events)

                if conflicting_events:
                    logger.debug(
                        f"Event {event_count+1}/{num_events_to_create} conflicts with {num_conflicting_events}..."
                    )
                    conflicting_event_ids = [
                        _conflict_event["id"]
                        for _conflict_event in conflicting_events
                    ]

                    match on_data_conflict:
                        case ConflictResolutionStrategy.FAIL:
                            logger.error(
                                (
                                    "Exiting process since "
                                    "on_data_conflict=`fail`..."
                                )
                            )
                            return {
                                "status_code": 409,
                                "msg": (
                                    f"At least one event to write conflicts with events from calendar=`{calendar_id}` on the following conflict properties `{data_conflict_properties}`"
                                ),
                                "data": [
                                    {
                                        "event_to_write": event,
                                        "event_id": event_id,
                                        "id_of_events_that_conflict": conflicting_event_ids,
                                    }
                                ],
                            }
                        case ConflictResolutionStrategy.IGNORE:
                            logger.info(
                                f"Dropping event_id `{event_id}` from request since on_data_conflict=`ignore`..."
                            )
                            conflict_events.append(
                                {
                                    "event_to_write": events_to_create.pop(
                                        event_id
                                    ),
                                    "event_id": event_id,
                                    "id_of_events_that_conflict": conflicting_event_ids,
                                }
                            )
                else:
                    logger.info(
                        f"Did not find any conflicts for event_id=`{event_id}`"
                    )

        if not events_to_create:
            _msg = "No events to create"
            logger.info(_msg)
            return_msg = {"msg": _msg, "status_code": 200}
            if (
                on_data_conflict == ConflictResolutionStrategy.IGNORE
                and conflict_events
            ):
                return_msg["data"] = [
                    {"ignored_events_due_to_conflict": conflict_events}
                ]

            return return_msg

        num_events_to_create = len(events_to_create)
        logger.info(f"Writing {num_events_to_create} events...")
        failed_writes = []
        for event_count, (event_id, event) in enumerate(
            events_to_create.items()
        ):
            try:
                events_session.insert(
                    calendarId=calendar_id, body=event
                ).execute()
            except HttpError as http_error:
                status_code = http_error.status_code
                logger.error(
                    (
                        f"Failed to create event {event_count+1}/{num_events_to_create}. "
                        f"Reason: {http_error}"
                    )
                )
                failed_writes.append(
                    {
                        "msg": http_error,
                        "data": {"event": event, "event_id": event_id},
                        "status_code": status_code,
                    }
                )

        num_failed_writes = len(failed_writes)
        if not failed_writes:
            _msg = f"Successfully wrote {num_events_to_create} events to calendar. No failures occurred in write process."
            logger.info(_msg)
            return_msg = {
                "msg": _msg,
                "status_code": 201,
            }

            if (
                on_data_conflict == ConflictResolutionStrategy.IGNORE
                and conflict_events
            ):
                return_msg["data"] = [
                    {"ignored_events_due_to_conflict": conflict_events}
                ]

        else:
            logger.info(f"{num_failed_writes} events failed to create")
            return_msg = {
                "data": [{"reason_for_failure": failed_writes}],
            }

            if num_failed_writes == num_events_to_create:
                _msg = "None of the events were successfully created due to write errors"
                logger.error(_msg)
                return_msg.update(
                    {
                        "msg": _msg,
                        "status_code": 400,
                    }
                )
            else:
                _msg = f"{num_failed_writes}/{num_events_to_create} events failed to create, but others were successful"
                logger.info(_msg)
                return_msg.update(
                    {
                        "msg": _msg,
                        "status_code": 207,
                    }
                )

            if (
                on_data_conflict == ConflictResolutionStrategy.IGNORE
                and conflict_events
            ):
                return_msg["data"].append(
                    {"ignored_events_due_to_conflict": conflict_events}
                )

        return return_msg

# -------------------
# CREATE EVENT
# ---------------------
CALENDAR_ID = 'hello@thyme.company'
DATA_CONFLICT_PROPERTIES = ['timeMin']
events = [
    {
        'summary': '🐋 Swim with Whales',
        'start': {
            'dateTime': '2024-04-24T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
            },
        'end': {
            'dateTime': '2024-04-24T19:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
            }
    }
]

client = GoogleCalendarClient()
print('CLIENT', client)

result = client.create_events(
    calendar_id=CALENDAR_ID, 
    events=events, 
    data_conflict_properties=DATA_CONFLICT_PROPERTIES
    )

print('RESULT', result)