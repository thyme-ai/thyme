from flask_wtf import FlaskForm;
from wtforms import SubmitField, StringField, IntegerField, TimeField, BooleanField
from wtforms.validators import DataRequired, Optional

optional = [Optional()]

class UpdateHabitForm(FlaskForm):
    name = StringField("Name of Habit", validators=optional)
    duration_min = IntegerField("Duration",validators=optional)
    ideal_start = TimeField("Ideal Start Time",validators=optional)
    personal = BooleanField("Personal Time?",validators=optional)
    submit = SubmitField("Submit")

