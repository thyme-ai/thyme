I'm working on making an OpenAPI function specification for the DELETE endpoint of the Google Calendar API. 
I want to expose this API endpoint to help an AI agent delete events from Google Calendar.

Can you help me convert the essential parts of the following documentation to an OpenAPI function specification that I can provide to a Custom GPT agent.

Here is the documentation: 
- OpenAPI 3 Specification - https://swagger.io/specification/
- Google Calendar API Events Resource - https://developers.google.com/calendar/api/v3/reference/events
- Google Calendar API Events DELETE endpoint - https://developers.google.com/calendar/api/v3/reference/events/delete

Remove any comments.
Add a property called {operationId} to each endpoint equal to the {summary} of the endpoint in snake case. 
Shorten the {operationId} to be as short as possible while still being descriptive, 
Remove the {calendarId} url and pass "primary" directly in the endpoint url.
Please output the result in the JSON OpenAPI 3 format, and provide the whole output JSON. If you need to split across messages, you can leave the JSON incomplete with "...". I will say "CONTINUE" and you can proceed in the next message.


