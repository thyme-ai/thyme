from app.models import db, User
from datetime import  time

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


def get_user_from_thyme(email):
   return db.one_or_404(db.select(User).filter_by(email=email))

