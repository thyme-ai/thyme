from flask_wtf import FlaskForm;
from wtforms import SubmitField, StringField, IntegerField, TimeField, BooleanField
from wtforms.validators import DataRequired, Optional

required = [DataRequired()]
optional = [Optional()]

class AddHabitForm(FlaskForm):
    name = StringField("Name of Habit", validators=required)
    duration_min = IntegerField("Duration",validators=required)
    ideal_start = TimeField("Ideal Start Time",validators=required)
    personal = BooleanField("Personal Time?",validators=optional)
    submit = SubmitField("Submit")

