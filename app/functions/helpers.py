from app.models import db, User, Habit
from flask import redirect, session, url_for
import google.oauth2.credentials
from datetime import time

# ------------------
# CREDENTIALS
# ------------------
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

# ------------------
# HABITS
# ------------------
def get_habit(habit_id):
    return db.session.execute(
        db.select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one()


def get_habits():
    user_id = get_user_id_or_create_new_user()
    habits = db.session.execute(
            db.select(Habit)
            .where(Habit.user_id == user_id)
            .order_by(Habit.name)
            ).scalars().all()
    return habits


# ------------------
# USERS
# ------------------
def create_user(email, first_name, last_name, profile_picture, timezone):
    user = User(
       email = email,
       first_name = first_name,
       last_name = last_name,
       profile_picture = profile_picture,
       timezone = timezone,
       wake_time = time(hour=7, minute=0),
       sleep_time = time(hour=22, minute=0),
       )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
   return db.one_or_404(db.select(User).filter_by(email=email))


def get_user_or_create_new_user():
    email = session['email']
    try:
      user = get_user_by_email(email)
    except:
      user = create_user()    
    return user


def get_user_id_or_create_new_user():
   user = get_user_or_create_new_user()
   return user.id





