# Thyme
Your personal AI assistant. Built with the OpenAI API, Google Calendar API, and Google Authentication.

<img src="https://storage.googleapis.com/frankie-esparza-portfolio/thumbnails/thyme.png" width="500">

## About
Thyme is an AI research company dedicated to building the most personal, useful, and private AI. Our personal AI assistant, Thyme, can schedule meetings, help you brainstorm, anticipate your needs, and more. Try the beta at [thyme.company](https://thyme.company)!
<br></br>

## Features 
### ✨ Schedule events in seconds 
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-1.gif" width="500">

### 🧠 Brainstorm with the power of AI
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-2.gif" width="500">

### 💭 Ask Thyme questions about your week
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-3.gif" width="500">
<br></br>

## Getting Started 
1. 💻 Go to [thyme.company](https://thyme.company) on a laptop or phone 
2. ✅ Login with Google to give Thyme acess to your Google Calendar (read our [Privacy Policy](https://thyme.company/privacy) & [Terms of Service](https://thyme.company/terms)) 
3. 🎉 You're all set to start using Thyme! Try saying:
- "Schedule a Coffee Chat with hello@thyme.company tomorrow at 10am"
- "What's on my calendar Friday?"
- "Schedule an event called Team Building this Thursday from 10am to 4pm, in the description add a few ideas of places to host a team building event in [insert your city here]"
<br></br>

## Contact
👋🏽 Have questions or feedback? We'd love to hear them! Send us an email at hello@thyme.company.
<br></br>

## Tutorials 
Want to learn more about building apps that use generative AI? Check out these articles!
- Getting started with the Google Calendar API - [HERE](https://developers.google.com/calendar/api/quickstart/python)
- Getting started with the Open AI API - [HERE](https://platform.openai.com/docs/quickstart)
- How to Call Functions with an OpenAPI Specification - [HERE](https://cookbook.openai.com/examples/function_calling_with_an_openapi_spec)
- How to Call Functions with Chat Models - [HERE](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)
- Guide to Prompt Engineering - [HERE](https://platform.openai.com/docs/guides/prompt-engineering)
<br></br>

## For Developers
### Running Thyme Locally
1) Download PostgreSQL (for macs, download the PostgreSQL app - [HERE](https://postgresapp.com/))
2) Download Python
3) Download Pipenv ```pip install pipenv```    
4) Create a Virtual Environment `pipenv install --python "$PYENV_ROOT/versions/<<version_name>>/bin/python"` (replace <<version_name>>)
5) Install all the dependencies for the Python App `pipenv install`
6) Create a `.env` file and copy & paste the contents of `.env.example`
- for the `DATABASE_URL` variable - use `.env.example`, replace all of the text in `<arrow-brackets>`
- for the `GOOGLE_CLIENT_CONFIG` variable - update this with your Google credentials, follow these instructions - [HERE](https://developers.google.com/calendar/api/quickstart/python)
7) Create the database:
```sql
cd thyme
psql    
DROP DATABASE thyme;
DROP USER thyme;  
CREATE USER thyme WITH PASSWORD '<insert-password-here>';    
CREATE DATABASE thyme WITH OWNER thyme;
```
8) Seed the database `python database.py`
9) Check that the data is in the database:
```sql
psql
SELECT * FROM habits;
\q
```
10) Start the local server `pipenv run flask run`
