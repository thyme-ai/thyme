import os.path
from app.models import db, Habit, User
from app.forms.updatePreferences import UpdatePreferencesForm
from app.forms.askQuestion import AskQuestionForm
from app.forms.addHabit import AddHabitForm
from app.forms.updateHabit import UpdateHabitForm
from app.functions.answer_question import answer_question
from flask import Blueprint, redirect, url_for, render_template
from google.oauth2.credentials import Credentials

bp = Blueprint("home", __name__, url_prefix="/")
SCOPES = [
    "https://www.googleapis.com/auth/calendar",         # edit calendar
    "https://www.googleapis.com/auth/userinfo.email",   # get email 
    "https://www.googleapis.com/auth/calendar.readonly" # get timezone
]

# ------------
# ROUTES
# ------------
@bp.route("/", methods=["GET"])
def index():
    if os.path.exists("token.json"):
        return redirect(url_for("home.assistant"))
    else:
        return render_template("welcome.html", title="Welcome")


@bp.route("/assistant", methods=["GET", "POST"])
def assistant():
    answer = None
    form = AskQuestionForm()
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.valid:
            if form.validate_on_submit():
                prompt = form.question.data
                answer = answer_question(prompt, creds)            
            return render_template("home.html", title="Home", form=form, form_type="one-line-form", justified_type="centered", answer=answer)
    return redirect(url_for("session.logout"))


@bp.route("/preferences", methods=["GET", "POST"])
def preferences():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.valid:
            user = getUser()
            habits = getHabits()
            return render_template("preferences.html", title="Preferences", habits=habits, user=user)
    return redirect(url_for("home.index"))

# ---------------
# HABITS
# ---------------
@bp.route("/addHabit", methods=["GET", "POST"])
def addHabit():
    form = AddHabitForm()

    if form.validate_on_submit():
       handleAddHabit(form)
       return redirect(url_for("home.preferences"))
    return render_template("/components/form.html", title="Add Habit", form=form, justified_type="left-justified")


@bp.route("/updateHabit/<habit_id>", methods=["GET", "POST"])
def updateHabit(habit_id):
    form = UpdateHabitForm()
    habit = getHabit(habit_id)

    if form.validate_on_submit():
        handleUpdateHabit(form, habit_id)
        return redirect(url_for("home.preferences"))
    return render_template("/components/form.html", title=habit.name,  form=form, justified_type="left-justified")


@bp.route("/deleteHabit/<habit_id>", methods=["GET", "DELETE"])
def deleteHabit(habit_id):
    handleDeleteHabit(habit_id)
    return redirect(url_for("home.preferences"))


@bp.route("/addHabitsToCalendar", methods=["GET", "POST"])
def addHabitsToCalendar():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        form=AskQuestionForm()
        if creds and creds.valid:
            habits = getHabits()
            habit_strings = map(lambda habit: f"called {habit.name} for {habit.duration_min} min at {habit.ideal_start.strftime('%-I:%M %p')}", habits)
            answer_strings = map(lambda habit: f"{habit.name}", habits)

            for habit_string in habit_strings:
                prompt = f"Add an event to my calendar that repeats every weekday {habit_string}"
                answer_question(prompt, creds) 
            
            answer = f"""
            I added these habits to your calendar: {(", ").join(answer_strings)}. 
            You might need to refresh Google Calendar to see them. """
            return render_template("home.html", title="Home", form=form, form_type="one-line-form", justified_type="centered", answer=answer)

    return redirect(url_for("session.logout"))



# ---------------
# PREFERENCES
# ---------------
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
def handleAddHabit(form):
    habit = Habit(
       name = form.name.data,
       duration_min = form.duration_min.data,
       ideal_start = form.ideal_start.data,
       personal = form.personal.data,
       user_id = getUserId()
       )
    db.session.add(habit)
    db.session.commit()


def handleDeleteHabit(habit_id):
    habit = getHabit(habit_id)
    db.session.delete(habit)
    db.session.commit()

def handleUpdateHabit(form, habit_id):
    habit = getHabit(habit_id)

    for field in form._fields.keys():
            data = form.data[field]
            if data != None and field != 'submit' and field != 'csrf_token' :
                setattr(habit, field, data)
                db.session.execute(
                    db.select(getattr(Habit, field))
                    .where(Habit.id == habit.id)).scalar_one()
    db.session.commit()


def handleUpdatePreferences(form):
    user = getUser() 
    for field in form._fields.keys():
            data = form.data[field]
            if data != None and field != 'submit' and field != 'csrf_token' :
                setattr(user, field, data)
                db.session.execute(
                    db.select(getattr(User, field))
                    .where(User.id == user.id)).scalar_one()
    db.session.commit()


# ------------
# HELPERS
# ------------
def getHabit(habit_id):
    return db.session.execute(
        db.select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one()


def getHabits():
    return db.session.execute(
        db.select(Habit)
        .where(Habit.user_id == getUserId())
        .order_by(Habit.name)
    ).scalars().all()

def getUserId():
   return db.session.execute(
        db.select(User)
        .where(User.gmail == "hello@thyme.company")
    ).scalar_one().id


def getUser():
    return db.session.execute(
        db.select(User)
        .where(User.id == getUserId())
    ).scalar_one()