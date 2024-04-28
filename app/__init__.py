from flask import Flask 
from .config import Configuration 
from .models import db
from .routes import habit, home, session

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(habit.bp)
app.register_blueprint(home.bp)
app.register_blueprint(session.bp)

db.init_app(app)