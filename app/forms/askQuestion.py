from flask_wtf import FlaskForm;
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea

required = [DataRequired()]
optional = [Optional()]

class AskQuestionForm(FlaskForm):
    question = TextAreaField("How can I help?", validators=required, widget=TextArea())
    submit = SubmitField("Submit")

