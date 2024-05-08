from app.models import db, Habit
from app.functions.thyme.helpers.user import get_user_from_thyme
from flask import session

def get_habit(habit_id):
    return db.session.execute(
        db.select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one()


def get_habits():
    user = get_user_from_thyme(session['email'])
    habits = db.session.execute(
            db.select(Habit)
            .where(Habit.user_id == user.id)
            .order_by(Habit.name)
            ).scalars().all()
    return habits



