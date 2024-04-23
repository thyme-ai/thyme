# Thyme
Thyme is a personal assistant that helps you run your day and get things done faster, so you can spend more time doing the things you love.

## Features 
1) **Chat Interface** to make it easy to manage your calendar via a chat interface
2) **Event Suggestions** to give you helpful suggestions for creative ideas for events
3) **Habit Scheduling** to make it easy to meet your work-life balance goals throughout the week

#### Thyme can help you schedule events,   
<img width="600" alt="Schedule Events" src="https://github.com/thyme-ai/thyme/assets/17794659/c5a23638-ecab-4b4d-b8f2-29213b0515cb">

#### answer questions,  
<img width="300" alt="Answer Questions" src="https://github.com/thyme-ai/thyme/assets/17794659/0ca19938-3a79-4519-bded-94f63ad89d5b">

#### and help you think of creative ideas.
<img width="600" alt="Suggest Ideas for Events" src="https://github.com/thyme-ai/thyme/assets/17794659/757c2008-5125-45e2-a8ab-bf705d6754ac">

## Tutorials Used
  - **Google Calendar API** 
    - Getting Started - [HERE](https://developers.google.com/calendar/api/quickstart/python)
  - **Open AI API**
    - Getting Started - [HERE](https://platform.openai.com/docs/quickstart)
    - How to Call Functions  with an OpenAPI Specification - [HERE](https://cookbook.openai.com/examples/function_calling_with_an_openapi_spec)
    - How to Call Functions with Chat Models - [HERE](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)
     - Guide to Prompt Engineering - [HERE](https://platform.openai.com/docs/guides/prompt-engineering)

## APIs, Libraries, & Frameworks Used 
### APIs
- **Google**
    - Google Calendar API
    - Google OAuth 2.0 for Authentication & Authorization
    - Google API Python Client
- **OpenAI API**


### Libraries & Frameworks
- **Python**
- **Flask** Python micro-framework used to make web apps 
- **Jinja** helps create templates for HTML content  
- **Database:**
    - **Flask-SQLAlchemy** Python SQL toolkit & ORM (Object Relational Mapper)
    - **PostgresQL** object-relational database system 
    - **psycopg2-binary** allows SQLAlchemy to connect to you PostgreSQL database
- **Forms:**
    - **Flask-WTF** wrapper around WTForms package that helps create HTML Forms in Python
    - **wtforms** for form validation & rendering
- **Package Management**
    - **pip** installs and manages software packages
    - **Pipenv** create virtual environments for python projects
    - **python-dotenv** allows Flask to use .env or .flaskenv files
   

## How to Run Thyme Locally
### Installation
1) PostgreSQL
- **For macs:** download the PostgreSQL app - [HERE](https://postgresapp.com/)
- **For non-macs:** download PostgresQL - [HERE]( https://www.postgresql.org/download/)  

2) Python 3.12.2 (or later) - [HERE](https://www.python.org/downloads/)

3) Pipenv ```pip install pipenv```    

4) Create a Virtual Environment (replace <<version_name>> with version of python you installed above) -  
```pipenv install --python "$PYENV_ROOT/versions/3.12.2/bin/python"```

5) Install all the dependencies for the Python App  
```pipenv install --python "$PYENV_ROOT/shims/python" psycopg2-binary Flask-SQLAlchemy alembic Flask-Migrate Flask python-dotenv Flask-WTF wtforms Jinja2```

6) Install Google client library for python -  
```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```

7) Install OpenAI Python Libray -  
```pip install --upgrade openai```

8) Create .env file 
```FLASK_ENV=development```
```SECRET_KEY=<insert-secret-key-here>```
```DATABASE_URL=postgresql://thyme:<insert-database-password-here>@localhost/thyme```    

9) Create .flaskenv file
```FLASK_APP=thyme.py```    


### Running the App
1) Create the PostgreSQL database:
cd into the 'thyme' directory
```psql```    
```DROP DATABASE thyme;```    
```DROP USER thyme;```    
```CREATE USER thyme WITH PASSWORD '<insert-password-here>';```    
```CREATE DATABASE thyme WITH OWNER thyme;```    
you should see output showing that the thyme user & database were created

2) Seed the database: 
```\q``` to exist out of psql
```python database.py``` to seed the database 
```psql```
```SELECT * FROM habits;``` to confirm the data was seeded successfully 
```\q``` to exit out of psql

3) Start the server: 
```pipenv run flask run```
Then click on the link that says something like "Running on http://"...

4) If prompted to log into Google Calendar, follow the prompts
(note that only google accounts that have been added by Thyme as test users in Google Cloud console can access the 
Thyme app. Email [hello@thyme.company](hello@thyme.company) if you'd like to be added as a test user.)
