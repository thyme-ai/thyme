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


def get_user():
    return db.session.execute(
        db.select(User)
        .where(User.id == get_user_id())
    ).scalar_one()


def get_user_id():
   return db.session.execute(
        db.select(User)
        .where(User.gmail == "hello@thyme.company")
    ).scalar_one().id