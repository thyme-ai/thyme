from app.models import User
from datetime import time

USER_FOR_TESTING = User(
    email = "hello@thyme.company",
    timezone = "America/Los_Angeles",
    wake_time = time(hour=7, minute=0),
    sleep_time = time(hour=22, minute=0),
)
