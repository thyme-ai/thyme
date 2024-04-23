I'm working on making an OpenAPI function specification for the LIST endpoint of the Google Calendar API. 
I want to expose this API endpoint to help an AI agent get multiple events from 
a Google Calendar. 

Can you help me convert the essential parts of the following documentation to an OpenAPI function specification that I can provide to a Custom GPT agent.

Here is the documentation: 
- OpenAPI 3 Specification -  https://swagger.io/specification/
- Google Calendar API Events Resource - https://developers.google.com/calendar/api/v3/reference/events
- Google Calendar API Events LIST endpoint - https://developers.google.com/calendar/api/v3/reference/events/list

The only properties that I care about for each event are: 
- {id}
- {htmlLink}
- {summary}
- {description}

- {start}
- {end}
- {timezone}
- {recurrence}

- {location}
- {organizer}
- {attendees}

I'd like to be able to search for events based on the following optional query
parameters
- {maxResults}
- {orderby}
- {q}
- {timeMin}
- {timeMax}

Remove any comments.
Add a property called {operationId} to each endpoint equal to the {summary} of the endpoint in snake case. 
Shorten the {operationId} to be as short as possible while still being descriptive, 
Remove the {calendarId} url and pass "primary" directly in the endpoint url.
Please output the result in the JSON OpenAPI 3 format, and provide the whole output JSON.  


