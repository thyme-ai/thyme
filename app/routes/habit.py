from app.models import db, Habit
from app.forms import AddHabitForm, UpdateHabitForm
from app.functions.openai.answer_question import answer_question
from app.functions.thyme.helpers.habits import get_habit, get_habits
from app.functions.thyme.helpers.user import get_user_from_thyme
from flask import Blueprint, redirect, url_for, render_template, session

bp = Blueprint("habit", __name__, url_prefix="/habit")

# -----------
# ADD 
# -----------
@bp.route("/add", methods=["GET", "POST"])
def add():
    form = AddHabitForm()
    if form.validate_on_submit():
       handle_add_habit(form)
       return redirect(url_for("home.preferences"))
    return render_template("/components/forms/form.html", title="Add Habit", form=form, justified_type="left-justified")

# -----------
# UPDATE 
# -----------
@bp.route("/update/<habit_id>", methods=["GET", "POST"])
def update(habit_id):
    form = UpdateHabitForm()
    habit = get_habit(habit_id)
    if form.validate_on_submit():
        handle_update_habit(form, habit_id)
        return redirect(url_for("home.preferences"))
    return render_template("/components/forms/form.html", title=habit.name,  form=form, justified_type="left-justified")

# -----------
# DELETE 
# -----------
@bp.route("/delete/<habit_id>", methods=["GET", "DELETE"])
def delete(habit_id):
    handle_delete_habit(habit_id)
    return redirect(url_for("home.preferences"))


# ------------------------
# ADD HABITS TO CALENDAR 
# ------------------------
@bp.route("/addHabitsToCalendar", methods=["GET", "POST"])
def addHabitsToCalendar():
        habits = get_habits()
        habit_strings = map(lambda habit: f"called {habit.name} for {habit.duration_min} min at {habit.ideal_start.strftime('%-I:%M %p')}", habits)
        answer_strings = map(lambda habit: f"{habit.name}", habits)

        for habit_string in habit_strings:
            prompt = f"Add an event to my calendar that repeats every weekday {habit_string}"
            answer_question(prompt) 
            
        answer = f"""
        I added these habits to your calendar: {(", ").join(answer_strings)}. 
        You might need to refresh Google Calendar to see them. """
        return redirect(url_for("home.assistant", answer=answer))


# ------------------------
# EVENT HANDLERS
# ------------------------
def handle_add_habit(form):
    user = get_user_from_thyme(session['email'])
    habit = Habit(
       name = form.name.data,
       duration_min = form.duration_min.data,
       ideal_start = form.ideal_start.data,
       personal = form.personal.data,
       user_id = user.id
       )
    db.session.add(habit)
    db.session.commit()


def handle_delete_habit(habit_id):
    habit = get_habit(habit_id)
    db.session.delete(habit)
    db.session.commit()


def handle_update_habit(form, habit_id):
    habit = get_habit(habit_id)
    for field in form._fields.keys():
            data = form.data[field]
            if data != None and field != 'submit' and field != 'csrf_token' :
                setattr(habit, field, data)
                db.session.execute(
                    db.select(getattr(Habit, field))
                    .where(Habit.id == habit.id)).scalar_one()
    db.session.commit()


