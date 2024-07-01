# Thyme
Meet Thyme, your personal AI assistant, built with the OpenAI API, Google Calendar API, & Google Authentication. Thyme can schedule meetings, help you brainstorm, anticipate your needs, and more. 

- ✨ Try the beta at [thyme.company](https://thyme.company)
- 🎬 Watch the Demo Video - [HERE](https://frankie.engineer/highlights)
- 🎬 Watch the "Resource Guide & Lessons Learned from Building Thyme" video - [HERE](https://www.youtube.com/watch?v=HDznguxTmtQ)
<br></br>

<img src="https://storage.googleapis.com/frankie-esparza-portfolio/thumbnails/thyme.png" width="500">

## Features 
### ✨ Schedule events in seconds 
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-1.gif" width="500">

### 🧠 Brainstorm with the power of AI
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-2.gif" width="500">

### 💭 Ask Thyme questions about your week
<img src="https://storage.googleapis.com/frankie-esparza-portfolio/gifs/thyme-3.gif" width="500">
<br></br>

## Getting Started 
1. Go to [thyme.company](https://thyme.company) on a 💻 laptop or 📱 phone 
2. Login with Google to give Thyme acess to your Google Calendar
3. You're all set to start using Thyme! Try saying:
- "Schedule a Coffee Chat with hello@thyme.company tomorrow at 10am"
- "What's on my calendar Friday?"
- "Schedule an event called Team Building this Thursday from 10am to 4pm, in the description add a few ideas of places to host a team building event in [insert your city here]"
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
<br></br>

## Contact
Questions or feedback? We'd love to hear what you think! Email [hello@thyme.company](https://mail.google.com/mail/u/0/?fs=1&to=fwesparza@gmail.com&tf=cm).
