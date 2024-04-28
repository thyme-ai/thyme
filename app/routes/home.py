import os.path
from app.models import db, User
from app.forms import AskQuestionForm, UpdatePreferencesForm
from app.functions.answer_question import answer_question
from flask import Blueprint, redirect, url_for, render_template
from flask import Blueprint, redirect, session, url_for, render_template
from app.functions.helpers import credentials_to_dict, check_for_credentials, get_habits, get_user

bp = Blueprint("home", __name__, url_prefix="/")

# ------------------------------
# WELCOME
# ------------------------------
@bp.route("/", methods=["GET"])
def index():
    if 'credentials' in session:
        return redirect(url_for("home.assistant"))
    else:
        return render_template("welcome.html", title="Welcome")


# ------------------------------
# HOME
# ------------------------------
@bp.route('/assistant', methods=["GET", "POST"])
def assistant():
  creds = check_for_credentials()
  answer = None
  form = AskQuestionForm()
  if form.validate_on_submit():
    prompt = form.question.data
    answer = answer_question(prompt, creds)    
  return render_template("home.html", title="Home", form=form, form_type="one-line-form", justified_type="centered", answer=answer)


# ------------------------------
# PREFERENCES
# ------------------------------
@bp.route("/preferences", methods=["GET", "POST"])
def preferences():
    user = get_user()
    habits = get_habits()
    return render_template("preferences.html", title="Preferences", habits=habits, user=user)

# ------------------------------
# UPDATE PREFERENCES
# ------------------------------
@bp.route("/updatePreferences", methods=["GET", "POST"])
def updatePreferences():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
       handleUpdatePreferences(form)
       return redirect(url_for("home.preferences"))
    return render_template("/components/form.html", title="Update Daily Schedule",  form=form, justified_type="left-justified")


# ---------------
# EVENT HANDLERS
# ---------------
def handleUpdatePreferences(form):
    user = get_user() 
    for field in form._fields.keys():
        data = form.data[field]
        if data != None and field != 'submit' and field != 'csrf_token' :
            setattr(user, field, data)
            db.session.execute(
                db.select(getattr(User, field))
                .where(User.id == user.id)).scalar_one()
    db.session.commit()
    