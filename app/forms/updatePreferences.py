from flask_wtf import FlaskForm;
from wtforms import SubmitField,TimeField, BooleanField
from wtforms.validators import DataRequired, Optional

default = [DataRequired()]
optional= [Optional()]

class UpdatePreferencesForm(FlaskForm):
    wake_time = TimeField("Usual Wake Up Time", validators=optional)
    sleep_time = TimeField("Usual Sleep Time", validators=optional)
    submit = SubmitField("Submit")

