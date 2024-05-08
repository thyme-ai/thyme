from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import ForeignKey
import uuid

db = SQLAlchemy()
uuid_type = UUID(as_uuid=True)

habits_per_user = db.Table(
    "habits_per_user",
    db.Model.metadata,
    db.Column("habit_id", uuid_type, db.ForeignKey("habits.id", ondelete="CASCADE"), primary_key=True),
    db.Column("user_id", uuid_type, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

messages_per_chat = db.Table(
    "messages_per_chat",
    db.Model.metadata,
    db.Column("message_id", uuid_type, db.ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True),
    db.Column("chat_id", uuid_type, db.ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(uuid_type, primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(100), unique=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    profile_picture = db.Column(db.String(2000), nullable=True)
    timezone = db.Column(db.String(100), nullable=False)

    wake_time = db.Column(db.Time, nullable=False)
    sleep_time = db.Column(db.Time, nullable=False)

    habits = db.relationship("Habit", secondary=habits_per_user, back_populates="user", cascade="all, delete")


class Habit(db.Model):
    __tablename__ = "habits"

    id = db.Column(uuid_type, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    duration_min = db.Column(db.Integer, nullable=True)
    ideal_start = db.Column(db.Time, nullable=True)
    personal = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(uuid_type, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(uuid_type, primary_key=True, default=uuid.uuid4)
    messages = db.relationship("Message", secondary=messages_per_chat, back_populates="chat", cascade="all, delete")

    user_id = db.Column(uuid_type, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(uuid_type, primary_key=True, default=uuid.uuid4)
    role = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    function_name = db.Column(db.String(100), nullable=True)
    function_call = db.Column(db.String(100), nullable=True)

    chat_id = db.Column(uuid_type, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    chat = db.relationship("Chat")

