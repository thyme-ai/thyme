I'm working on making an OpenAPI function specification for the DELETE, GET, INSERT, LIST, and PATCH endpoints of the Google Calendar API. I want to expose these API endpoints to help an AI agent manipulate a Google Calendar.

Please combine the following function specifications into a single function specification and output the result in the JSON OpenAPI 3 format, and provide the whole output JSON.  

Here is the specification for the DELETE endpoint in JSON:
{
    "openapi": "3.0.0",
    "info": {
      "title": "Custom GPT Google Calendar API",
      "version": "1.0.0",
      "description": "Custom GPT agent for Google Calendar API"
    },
    "servers": [
      {
        "url": "https://www.googleapis.com/calendar/v3/calendars/primary/"
      }
    ],
    "paths": {
      "/events/{eventId}": {
        "delete": {
          "summary": "Delete Event",
          "operationId": "delete_event",
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
          "responses": {
            "204": {
              "description": "Event deleted successfully"
            },
            "404": {
              "description": "Event not found"
            },
            "410": {
              "description": "Event already deleted"
            }
          }
        }
      }
    }
  }

Here is the specification for the GET endpoint in JSON:

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "version": "1.0.0",
    "description": "Custom GPT agent integration for Google Calendar API"
  },
  "paths": {
    "/events/{eventId}": {
      "get": {
        "summary": "Get Event",
        "operationId": "get_event",
        "parameters": [
          {
            "name": "eventId",
            "in": "path",
            "required": true,
            "description": "ID of the event to retrieve",
            "schema": {
              "type": "string"
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
                    "summary": {
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
                    "location": {
                      "type": "string"
                    },
                    "description": {
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
                          "responseStatus": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "recurrence": {
                      "type": "array",
                      "items": {
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

Here is the specification for the INSERT endpoint in JSON:

{
  "openapi": "3.0.0",
  "info": {
    "title": "Google Calendar API",
    "version": "1.0.0",
    "description": "Custom GPT Agent OpenAPI Specification for Google Calendar API Events"
  },
  "servers": [
    {
      "url": "https://www.googleapis.com/calendar/v3/calendars/primary"
    }
  ],
  "paths": {
    "/events": {
      "post": {
        "summary": "Insert Event",
        "operationId": "insert_event",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "summary": {
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
                    },
                    "required": ["dateTime", "timeZone"]
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
                    },
                    "required": ["dateTime", "timeZone"]
                  },
                  "timezone": {
                    "type": "string"
                  },
                  "location": {
                    "type": "string"
                  },
                  "description": {
                    "type": "string"
                  },
                  "organizer": {
                    "type": "object",
                    "properties": {
                      "email": {
                        "type": "string"
                      }
                    },
                    "required": ["email"]
                  },
                  "attendees": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "email": {
                          "type": "string"
                        }
                      },
                      "required": ["email"]
                    }
                  },
                  "recurrence": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    }
                  }
                },
                "required": ["summary", "start", "end", "timezone", "organizer"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Event Inserted Successfully"
          }
        }
      }
    }
  }
}

Here is the specification for the LIST endpoint in JSON:

{
    "openapi": "3.0.0",
    "info": {
      "title": "Google Calendar API",
      "version": "1.0.0"
    },
    "paths": {
      "/events": {
        "get": {
          "summary": "List events",
          "operationId": "list_events",
          "parameters": [
            {
              "name": "timeMin",
              "in": "query",
              "description": "Lower bound (exclusive) for an event's start time to filter by.",
              "required": false,
              "schema": {
                "type": "string",
                "format": "date-time"
              }
            },
            {
              "name": "timeMax",
              "in": "query",
              "description": "Upper bound (exclusive) for an event's end time to filter by.",
              "required": false,
              "schema": {
                "type": "string",
                "format": "date-time"
              }
            },
            {
              "name": "maxResults",
              "in": "query",
              "description": "Maximum number of events returned on one result page.",
              "required": false,
              "schema": {
                "type": "integer",
                "format": "int32",
                "minimum": 1,
                "maximum": 2500
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
                            "summary": {
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
                            "location": {
                              "type": "string"
                            },
                            "description": {
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
                            },
                            "recurrence": {
                              "type": "array",
                              "items": {
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

Here is the specification for the PATCH endpoint in JSON:

{
    "openapi": "3.0.0",
    "info": {
      "title": "Google Calendar API",
      "version": "v3"
    },
    "paths": {
      "/calendar/v3/events/{eventId}": {
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
        "patch": {
          "summary": "Update Event",
          "operationId": "update_event",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "summary": {
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
                    "location": {
                      "type": "string"
                    },
                    "description": {
                      "type": "string"
                    },
                    "organizer": {
                      "type": "object",
                      "properties": {
                        "email": {
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
                          }
                        }
                      }
                    },
                    "recurrence": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "Successful update of event."
            }
          }
        }
      }
    }
  }
  
  





  
