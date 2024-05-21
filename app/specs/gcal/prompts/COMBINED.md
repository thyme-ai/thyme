I'm working on making an OpenAPI function specification for the DELETE, GET, INSERT, LIST, and UPDATE endpoints of the Google Calendar API. I want to expose these API endpoints to help an AI agent manipulate a Google Calendar.

Please combine the following function specifications into a single function specification and output the result in the JSON OpenAPI 3 format, and provide the whole output JSON. If you need to split across messages, you can leave the JSON incomplete with "...". I will say "CONTINUE" and you can proceed in the next message.

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "description": "API for managing Google Calendar events",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    }
  ],
  "paths": {
    "/{eventId}": {
      "delete": {
        "summary": "Delete Event",
        "operationId": "delete_event",
        "parameters": [
          {
            "name": "eventId",
            "in": "path",
            "required": true,
            "description": "ID of the event to delete",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Event deleted successfully"
          },
          "404": {
            "description": "Event not found"
          },
          "500": {
            "description": "Internal server error"
          }
        }
      }
    }
  }
}

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "version": "1.0.0",
    "description": "Custom GPT Agent API Specification for Google Calendar"
  },
  "servers": [
    {
      "url": "https://www.googleapis.com/calendar/v3/calendars/primary"
    }
  ],
  "paths": {
    "/events/{eventId}": {
      "parameters": [
        {
          "name": "eventId",
          "in": "path",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      ],
      "get": {
        "summary": "Get Event",
        "operationId": "get_event",
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string"
                    },
                    "htmlLink": {
                      "type": "string"
                    },
                    "summary": {
                      "type": "string"
                    },
                    "description": {
                      "type": "string"
                    },
                    "start": {
                      "type": "object",
                      "properties": {
                        "dateTime": {
                          "type": "string",
                          "format": "date-time"
                        },
                        "timeZone": {
                          "type": "string"
                        }
                      }
                    },
                    "end": {
                      "type": "object",
                      "properties": {
                        "dateTime": {
                          "type": "string",
                          "format": "date-time"
                        },
                        "timeZone": {
                          "type": "string"
                        }
                      }
                    },
                    "timezone": {
                      "type": "string"
                    },
                    "recurrence": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "location": {
                      "type": "string"
                    },
                    "organizer": {
                      "type": "object",
                      "properties": {
                        "email": {
                          "type": "string"
                        },
                        "displayName": {
                          "type": "string"
                        }
                      }
                    },
                    "attendees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "email": {
                            "type": "string"
                          },
                          "displayName": {
                            "type": "string"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "version": "v3"
  },
  "paths": {
    "/events/insert": {
      "post": {
        "summary": "Insert Event",
        "operationId": "insert_event",
        "description": "Creates a new event.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Event"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Event"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Event": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier for the event."
          },
          "htmlLink": {
            "type": "string",
            "description": "URL link to the Google Calendar event."
          },
          "summary": {
            "type": "string",
            "description": "Title of the event."
          },
          "description": {
            "type": "string",
            "description": "Description of the event."
          },
          "start": {
            "$ref": "#/components/schemas/DateTime",
            "description": "The start time of the event."
          },
          "end": {
            "$ref": "#/components/schemas/DateTime",
            "description": "The end time of the event."
          },
          "timezone": {
            "type": "string",
            "description": "The time zone of the event."
          },
          "recurrence": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "List of RRULE, RDATE, and EXDATE lines for a recurring event."
          },
          "location": {
            "type": "string",
            "description": "The location of the event."
          },
          "organizer": {
            "$ref": "#/components/schemas/Person",
            "description": "The organizer of the event."
          },
          "attendees": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Person"
            },
            "description": "List of attendees for the event."
          }
        }
      },
      "DateTime": {
        "type": "object",
        "properties": {
          "dateTime": {
            "type": "string",
            "format": "date-time",
            "description": "The date and time of the event."
          },
          "timeZone": {
            "type": "string",
            "description": "The time zone of the event."
          }
        }
      },
      "Person": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "description": "Email address of the person."
          }
        }
      }
    }
  }
}

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "description": "Custom API specification for interacting with Google Calendar events.",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://www.googleapis.com/calendar/v3/calendars/primary/"
    }
  ],
  "paths": {
    "/events": {
      "get": {
        "summary": "List events",
        "operationId": "list_events",
        "description": "Returns events on the user's primary calendar.",
        "parameters": [
          {
            "name": "eventTypes",
            "in": "query",
            "description": "Type of events to be returned.",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "maxResults",
            "in": "query",
            "description": "Maximum number of events to return.",
            "required": false,
            "schema": {
              "type": "integer",
              "format": "int32"
            }
          },
          {
            "name": "orderby",
            "in": "query",
            "description": "Field by which to sort the list of events.",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "q",
            "in": "query",
            "description": "Search keywords.",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "timeMin",
            "in": "query",
            "description": "Minimum start time of events to return (exclusive).",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            }
          },
          {
            "name": "timeMax",
            "in": "query",
            "description": "Maximum end time of events to return (exclusive).",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "items": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string"
                          },
                          "htmlLink": {
                            "type": "string"
                          },
                          "summary": {
                            "type": "string"
                          },
                          "description": {
                            "type": "string"
                          },
                          "start": {
                            "type": "object",
                            "properties": {
                              "dateTime": {
                                "type": "string",
                                "format": "date-time"
                              },
                              "timeZone": {
                                "type": "string"
                              }
                            }
                          },
                          "end": {
                            "type": "object",
                            "properties": {
                              "dateTime": {
                                "type": "string",
                                "format": "date-time"
                              },
                              "timeZone": {
                                "type": "string"
                              }
                            }
                          },
                          "timezone": {
                            "type": "string"
                          },
                          "recurrence": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "location": {
                            "type": "string"
                          },
                          "organizer": {
                            "type": "object",
                            "properties": {
                              "email": {
                                "type": "string"
                              },
                              "displayName": {
                                "type": "string"
                              }
                            }
                          },
                          "attendees": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "email": {
                                  "type": "string"
                                },
                                "displayName": {
                                  "type": "string"
                                },
                                "organizer": {
                                  "type": "boolean"
                                },
                                "self": {
                                  "type": "boolean"
                                },
                                "responseStatus": {
                                  "type": "string"
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API Update Event",
    "version": "1.0.0"
  },
  "paths": {
    "/calendars/primary/events/{eventId}": {
      "put": {
        "summary": "Update Event",
        "operationId": "update_event",
        "description": "Creates a new event.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Event"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Event"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Event": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier for the event."
          },
          "htmlLink": {
            "type": "string",
            "description": "URL link to the Google Calendar event."
          },
          "summary": {
            "type": "string",
            "description": "Title of the event."
          },
          "description": {
            "type": "string",
            "description": "Description of the event."
          },
          "start": {
            "$ref": "#/components/schemas/DateTime",
            "description": "The start time of the event."
          },
          "end": {
            "$ref": "#/components/schemas/DateTime",
            "description": "The end time of the event."
          },
          "timezone": {
            "type": "string",
            "description": "The time zone of the event."
          },
          "recurrence": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "List of RRULE, RDATE, and EXDATE lines for a recurring event."
          },
          "location": {
            "type": "string",
            "description": "The location of the event."
          },
          "organizer": {
            "$ref": "#/components/schemas/Person",
            "description": "The organizer of the event."
          },
          "attendees": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/Person"
            },
            "description": "List of attendees for the event."
          }
        }
      },
      "DateTime": {
        "type": "object",
        "properties": {
          "dateTime": {
            "type": "string",
            "format": "date-time",
            "description": "The date and time of the event."
          },
          "timeZone": {
            "type": "string",
            "description": "The time zone of the event."
          }
        }
      },
      "Person": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "description": "Email address of the person."
          }
        }
      }
    }
  }
}
