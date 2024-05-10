from app.models import db, User
from app.forms import AskQuestionForm, UpdatePreferencesForm
from app.functions.openai.answer_question import answer_question
from app.functions.openai.utils.save_chat import save_chat
from app.functions.thyme.helpers.habits import get_habits
from app.functions.thyme.helpers.user import get_user_from_thyme
from flask import Blueprint, redirect, session, url_for, render_template

bp = Blueprint("home", __name__, url_prefix="/")
APOLOGY_STRING = "Sorrry, I'm not able to do that yet."    

# --------------------
# WELCOME
# --------------------
@bp.route("/", methods=["GET"])
def index():
    return render_template("welcome.html", title="Welcome")


# --------------------
# HOME
# --------------------
@bp.route('/assistant/', methods=["GET", "POST"])
@bp.route('/assistant/<answer>', methods=["GET", "POST"])
def assistant(answer = None): 
  if 'credentials' not in session:
      return redirect(url_for("home.index"))
  
  form = AskQuestionForm()
  if form.validate_on_submit():
    prompt = form.question.data
    user = get_user_from_thyme(session['email'])
    messages = answer_question(prompt, user)
    save_chat(messages, user)
    answer = messages[len(messages) - 1]['content']
  return render_template("home.html", title="Home", form=form, form_type="one-line-form", justified_type="centered", answer=answer)


# --------------------
# PREFERENCES
# --------------------
@bp.route("/preferences", methods=["GET", "POST"])
def preferences():
    user =get_user_from_thyme(session['email'])
    habits = get_habits()
    return render_template("preferences.html", title="Preferences", habits=habits, user=user)


# --------------------
# UPDATE PREFERENCES
# --------------------
@bp.route("/updatePreferences", methods=["GET", "POST"])
def updatePreferences():
    form = UpdatePreferencesForm()
    if form.validate_on_submit():
       handleUpdatePreferences(form)
       return redirect(url_for("home.preferences"))
    return render_template("/components/forms/form.html", title="Update Daily Schedule",  form=form, justified_type="left-justified")


# --------------------
# EVENT HANDLERS
# --------------------
def handleUpdatePreferences(form):
    user = get_user_from_thyme(session['email'])
 
    for field in form._fields.keys():
        data = form.data[field]
        if data != None and field != 'submit' and field != 'csrf_token' :
            setattr(user, field, data)
            db.session.execute(
                db.select(getattr(User, field))
                .where(User.id == user.id)).scalar_one()
    db.session.commit()


# --------------------
# ERRORS
# --------------------
@bp.errorhandler(404)
@bp.errorhandler(500)
def page_not_found(error):
    if 'credentials' not in session:
      return redirect(url_for("home.index"))
    form = AskQuestionForm()
    return render_template("home.html", title="Home", form=form, form_type="one-line-form", justified_type="centered", answer=APOLOGY_STRING)
    