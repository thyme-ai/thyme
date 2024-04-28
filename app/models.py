from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import ForeignKey

db = SQLAlchemy()

habits_per_user = db.Table(
    "habits_per_user",
    db.Model.metadata,
    db.Column("habit_id", db.Integer, db.ForeignKey("habits.id", ondelete="CASCADE"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(30), unique=True)
    wake_time = db.Column(db.Time, nullable=False)
    sleep_time = db.Column(db.Time, nullable=False)

    habits = db.relationship("Habit", secondary=habits_per_user, back_populates="user", cascade="all, delete")


class Habit(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    duration_min = db.Column(db.Integer, nullable=True)
    ideal_start = db.Column(db.Time, nullable=True)
    personal = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")

