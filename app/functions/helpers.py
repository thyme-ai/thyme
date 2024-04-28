from app.models import db, User, Habit
from flask import redirect, session, url_for
import google.oauth2.credentials

def check_for_credentials():
    if 'credentials' not in session:
        return redirect(url_for("session.login"))
    creds = google.oauth2.credentials.Credentials(**session['credentials'])
    return creds


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def getEmail(credentials):
    pass


def get_habit(habit_id):
    return db.session.execute(
        db.select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one()


def get_habits():
    return db.session.execute(
        db.select(Habit)
        .where(Habit.user_id == get_user_id())
        .order_by(Habit.name)
    ).scalars().all()


def get_user_or_create_new_user():
    user_id = get_user_id()
    user = None

    if not user_id:
        user = create_user()

    return user

def create_user():
    user = User(
       gmail = session['email'],
       wake_time = time(hour=7, minute=0),
       sleep_time = time(hour=7, minute=0),
       )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_id():
   email = session['email']
   
   return db.session.execute(
        db.select(User)
        .where(User.gmail == email)
    ).scalar_one().id