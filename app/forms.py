from flask_wtf import FlaskForm;
from wtforms import BooleanField, IntegerField, SubmitField, StringField, TextAreaField, TimeField 
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea
from app.functions.thyme.helpers.user import get_user_from_thyme
from flask import session

required = [DataRequired()]
optional = [Optional()]

LABEL_HABIT = "Name of Habit"
LABEL_DURATION = "Duration (minutes)"
LABEL_START = "Ideal Start Time"
LABEL_PERSONAL = "Personal Time?"
LABEL_SUBMIT = "Submit"


class AddHabitForm(FlaskForm):
    name = StringField(LABEL_HABIT, validators=required)
    duration_min = IntegerField(LABEL_DURATION,validators=required)
    ideal_start = TimeField(LABEL_START,validators=required)
    personal = BooleanField(LABEL_PERSONAL,validators=optional)
    submit = SubmitField(LABEL_SUBMIT)


class AskQuestionForm(FlaskForm):
    question = TextAreaField(
        validators=required, 
        widget=TextArea(), 
        render_kw={"placeholder": "How can I help?"}
    )
    submit = SubmitField(LABEL_SUBMIT)


class UpdateHabitForm(FlaskForm):
    name = StringField(LABEL_HABIT, validators=optional)
    duration_min = IntegerField(LABEL_DURATION,validators=optional)
    ideal_start = TimeField(LABEL_START,validators=optional)
    personal = BooleanField(LABEL_PERSONAL,validators=optional)
    submit = SubmitField(LABEL_SUBMIT)


class UpdatePreferencesForm(FlaskForm):
    wake_time = TimeField("Usual Wake Up Time", validators=optional)
    sleep_time = TimeField("Usual Sleep Time", validators=optional)
    submit = SubmitField(LABEL_SUBMIT)
