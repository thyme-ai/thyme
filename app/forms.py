from flask_wtf import FlaskForm;
from wtforms import BooleanField, IntegerField, SubmitField, StringField, TextAreaField, TimeField 
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea

required = [DataRequired()]
optional = [Optional()]


class AddHabitForm(FlaskForm):
    name = StringField("Name of Habit", validators=required)
    duration_min = IntegerField("Duration",validators=required)
    ideal_start = TimeField("Ideal Start Time",validators=required)
    personal = BooleanField("Personal Time?",validators=optional)
    submit = SubmitField("Submit")


class AskQuestionForm(FlaskForm):
    question = TextAreaField("How can I help?", validators=required, widget=TextArea())
    submit = SubmitField("Submit")


class UpdateHabitForm(FlaskForm):
    name = StringField("Name of Habit", validators=optional)
    duration_min = IntegerField("Duration",validators=optional)
    ideal_start = TimeField("Ideal Start Time",validators=optional)
    personal = BooleanField("Personal Time?",validators=optional)
    submit = SubmitField("Submit")


class UpdatePreferencesForm(FlaskForm):
    wake_time = TimeField("Usual Wake Up Time", validators=optional)
    sleep_time = TimeField("Usual Sleep Time", validators=optional)
    submit = SubmitField("Submit")
