from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import ForeignKey
from datetime import datetime, UTC
from uuid import uuid4

UUID_TYPE = UUID(as_uuid=True)
CURRENT_TIMESTAMP = datetime.now(UTC)

db = SQLAlchemy()

habits_per_user = db.Table(
    "habits_per_user",
    db.Model.metadata,
    db.Column("habit_id", UUID_TYPE, db.ForeignKey("habits.id", ondelete="CASCADE"), primary_key=True),
    db.Column("user_id", UUID_TYPE, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

messages_per_chat = db.Table(
    "messages_per_chat",
    db.Model.metadata,
    db.Column("message_id", UUID_TYPE, db.ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True),
    db.Column("chat_id", UUID_TYPE, db.ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID_TYPE, primary_key=True, default=uuid4)
    created = db.Column(db.DateTime, default=CURRENT_TIMESTAMP, nullable=False)
    updated = db.Column(db.DateTime, default=CURRENT_TIMESTAMP, onupdate=CURRENT_TIMESTAMP, nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.created:
            self.created = CURRENT_TIMESTAMP


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    profile_picture = db.Column(db.String(2000), nullable=True)
    timezone = db.Column(db.String(100), nullable=False)

    wake_time = db.Column(db.Time, nullable=False)
    sleep_time = db.Column(db.Time, nullable=False)

    habits = db.relationship("Habit", secondary=habits_per_user, back_populates="user", cascade="all, delete")


class Habit(BaseModel):
    __tablename__ = "habits"

    name = db.Column(db.String(100), nullable=False)
    duration_min = db.Column(db.Integer, nullable=True)
    ideal_start = db.Column(db.Time, nullable=True)
    personal = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")


class Chat(BaseModel):
    __tablename__ = "chats"

    messages = db.relationship("Message", secondary=messages_per_chat, back_populates="chat", cascade="all, delete")

    user_id = db.Column(UUID_TYPE, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")


class Message(BaseModel):
    __tablename__ = "messages"

    role = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    function_name = db.Column(db.String(100), nullable=True)
    function_call = db.Column(db.String(5000), nullable=True)

    chat_id = db.Column(UUID_TYPE, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    chat = db.relationship("Chat")

