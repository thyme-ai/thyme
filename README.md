# Thyme
Thyme is a personal assistant that helps you run your day and get things done faster, so you can spend more time doing the things you love. 

## Features 
1) **Chat Interface** to make it easy to manage your calendar & get helpful information via a chat interface
2) **Event Suggestions** to give you helpful suggestions for creative ideas when you're short on time for planning an event
3) **Habit Scheduling** to make it easy to meet your work-life balance goals throughout the week         
    
Thyme can help you **schedule events**.      
<img width="900" alt="Schedule Events" src="https://github.com/thyme-ai/thyme/assets/17794659/18ee21a1-a59b-46e8-b943-dc15447b5b07">
    

Thyme can **answer questions**.    
<img width="729" alt="Answer Questions" src="https://github.com/thyme-ai/thyme/assets/17794659/57aa57c1-ec53-48b3-8dd0-01cf139ed0c9">

Thyme can **think of creative ideas**.         
    
<img width="1777" alt="Suggest Ideas for Events - 1" src="https://github.com/thyme-ai/thyme/assets/17794659/fc62910b-726e-417d-b3f0-80266687d74b">

    
<img width="1742" alt="Suggest Ideas for Events - 2" src="https://github.com/thyme-ai/thyme/assets/17794659/5c77d035-52f0-401c-9bcd-a23c3ce080ad">

# For Developers:
## Setup 

### Download the Following
1) PostgreSQL
- **For macs:** download the PostgreSQL app https://postgresapp.com/
- **For non-macs:** download PostgresQL https://www.postgresql.org/download/    

2) Python 3.12.2 (or later) - https://www.python.org/downloads/    

3) Pipenv ```pip install pipenv```    

4) Create a Virtual Environment (replace <<version_name>> with version of python you installed above) -  
```pipenv install --python "$PYENV_ROOT/versions/«version_name»/bin/python"```

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


## How to Use the App
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
Then click on the link that says something like "Running on http://{some numbers}"

4) If prompted to log into Google Calendar, follow the prompts
(note that only emails that were added by the Thyme Google Organization to the Google Cloud console
can login to the Thyme app)

5) Click the **Settings** ⚙️ icon to fill out your user settings

6) Click  **Optimize Calendar** button to add your personal & work habits to your calendar 


## Reference 
**Libraries & Frameworks Used in this App**
- **Flask** is a back-end micro-framework used to make python web apps 
- **Jinja** helps create templates for HTML content  
- **pip** package-management system that installs and manages software packages
- **Pipenv** create virtual environments for python projects
- **python-dotenv** allows you to put environment files in a .env or .flaskenv file that Flask will use
- **Database:**
    - **Flask-SQLAlchemy** will integrate SQLAlchemy into your Flask application  
    - **PostgresQL** is an object-relational database system 
    - **psycopg2-binary** will allow SQLAlchemy to connect to you PostgreSQL database
- **Forms:**
    - **Flask-WTF** is a thin wrapper around WTForms package that helps create HTML Forms in Python
    - **wtforms** is a forms validation & rendering library for python

**Setting up a python app that calls a Google Workspace API**  
https://developers.google.com/calendar/api/quickstart/python?hl=en

**Setting up a python app that calls an Open AI API**  
https://platform.openai.com/docs/quickstart?context=python
