from dotenv import load_dotenv
from datetime import time
load_dotenv()

from app import app, db
from app.models import User, Habit

with app.app_context():
    db.drop_all()
    db.create_all()

    # -----------
    # Users
    # -----------
    user1 = User(
        gmail="hello@thyme.company",
        wake_time = time(hour=7, minute=0),
        sleep_time = time(hour=22, minute=0),
    )
    users = [user1]


    # -----------
    # Habits 
    # -----------
    walk_dog = Habit(
        name = "🐻 Walk Euler",
        duration_min = 60,
        ideal_start = time(hour=7, minute=30),
        personal = True,
        user = user1,
    )

    workout = Habit(
        name = "💪🏽 Workout",
        duration_min = 60,
        ideal_start = time(hour=11, minute=0),
        personal = True,
        user = user1,
    )

    yoga = Habit(
        name = "🧘🏽‍♀️ Yoga",
        duration_min = 15,
        ideal_start = time(hour=15, minute=0),
        personal = True,
        user = user1,
    )

    focus = Habit(
        name = "🧠 Focus",
        duration_min = 120,
        ideal_start = time(hour=13, minute=0),
        personal = False,
        user = user1,
    )

    habits = [walk_dog, workout, yoga, focus]

    # -----------
    # Seed the Data 
    # -----------
    data = [*users, *habits]

    for d in data:
        db.session.add(d)
    db.session.commit()