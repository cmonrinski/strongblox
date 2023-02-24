# create a web app that can create and record workout routines
import sqlite3
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)
app.secret_key = "dev"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect SQLite to database
db = sqlite3.connect("workouts.db")

CHAINS = ["Anterior", "Posterior", "Compound"]
FOCUSES = ["Lower", "Middle", "Upper"]
ANTIROTATIONS = ["None", "Single Arm", "Single Leg", "Twist", "Pallof"]

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def login_required(f):
    """
    Comment from CS50: 
    Decorate routes to require login. 
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/equipment", methods=["GET", "POST"])
@login_required
def equipment():
    if request.method == "POST":

        # Add equipment to equipment database
        equipment = request.form.get("equipment")

        # Remember equipment to database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute(
            "INSERT INTO equipments (equipment, user_id) VALUES(?,?)", (equipment, session["user_id"]))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/equipment")

    else:
        # Display all equipments in database from SQLite on equipment.html
        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM equipments WHERE user_id IS NULL OR user_id = ? ORDER BY equipment", (session["user_id"],))
        equipments = cur.fetchall()

        return render_template("equipment.html", equipments=equipments)


@app.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    if request.method == "POST":

        # Add exercise to exercise database
        exercise = request.form.get("exercise")
        variation = request.form.get("variation")
        focus = request.form.get("focus")
        muscle = request.form.get("muscle")
        chain = request.form.get("chain")

        # Remember exercise to database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute("INSERT INTO exercises (exercise, variation, focus, muscle, chain, user_id) VALUES(?,?,?,?,?,?)",
                    (exercise, variation, focus, muscle, chain, session["user_id"]))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/exercises")

    else:

        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()

        # Display all muscles in dropdown menu selection
        cur.execute("SELECT muscle FROM muscles WHERE user_id IS NULL OR user_id = ?", (session["user_id"],))
        muscles = cur.fetchall()

        # Display all exercises in database from SQLite on exercises.html
        cur.execute("SELECT * FROM exercises WHERE user_id IS NULL OR user_id = ?", (session["user_id"],))
        exercises = cur.fetchall()

        return render_template("exercises.html", exercises=exercises, muscles=muscles, chains=CHAINS, focuses=FOCUSES, antirotations=ANTIROTATIONS)


@app.route("/muscles", methods=["GET", "POST"])
@login_required
def muscles():
    if request.method == "POST":

        # Add muscle to muscles database
        muscle = request.form.get("muscle")

        # Remember muscle to database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute("INSERT INTO muscles (muscle, user_id) VALUES(?,?)", (muscle, session["user_id"]))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/muscles")

    else:
        # Display all muscles in database from SQLite on muscles.html
        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM muscles WHERE user_id IS NULL OR user_id = ? ORDER BY muscle", (session["user_id"],))
        muscles = cur.fetchall()

        return render_template("muscles.html", muscles=muscles)


@app.route("/routine", methods=["GET", "POST"])
@login_required
def routine():
    if request.method == "POST":

        form_data = request.get_json()

        date = datetime.today().strftime("%b %d, %Y")
        time = datetime.today().strftime("%H:%M")

        workout = []

        for i in range(0, len(form_data), 8):
            routine = list(form_data.values())[i:i+8]
            workout.insert(0, routine)

        for routine in workout:
            exercise = routine[0]
            variation = routine[1]
            antiroation = routine[2]
            equipment = routine[3]
            sets = routine[4]
            reps = routine[5]
            weight = routine[6]
            notes = routine[7]

            # Remember routine to database
            db = sqlite3.connect("workouts.db")
            cur = db.cursor()
            cur.execute("INSERT INTO routine (date, time, exercise, variation, antirotation, equipment, sets, reps, weight, notes, user_id) \
                VALUES(?,?,?,?,?,?,?,?,?,?,?)", 
                (date, time, exercise, variation, antiroation, equipment, sets, reps, weight, notes, session["user_id"]))

            # Commit changes and close connection
            db.commit()
        db.close()

        return redirect("/success")

    else:

        # Connecting to SQLite
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()

        # Get list of exercises for dropdown menu selection
        cur.execute("SELECT DISTINCT exercise FROM exercises WHERE user_id IS NULL OR user_id = ? ORDER BY exercise", (session["user_id"],))
        exercises = cur.fetchall()

        # Get list of variations for each exercise and store as dictionary of tuples with tuples
        # e.g. 'Exercise': [(exercise_id1, variation1), (exercise_id2, variation2)]
        variations = {}
        for exercise in exercises:
            cur.execute("SELECT exercise_id, variation FROM exercises WHERE exercise = ? AND (user_id IS NULL OR user_id = ?) ORDER BY exercise, variation", (exercise[0], session["user_id"]))
            temp = cur.fetchall()
            variations[exercise[0]] = temp

        # Display all equipment in dropdown menu selection
        cur.execute("SELECT equipment FROM equipments WHERE user_id IS NULL OR user_id = ? ORDER BY equipment", (session["user_id"],))
        equipments = cur.fetchall()

        # Get routine history to provide placeholders with dynamic data in routine table setup
        # Provides list of tuple e.g.: [(exercise, variation, ..., notes), (exercise, varaition, ..., notes)]
        cur.execute("SELECT exercise, variation, antirotation, equipment, sets, reps, weight, notes FROM routine \
            WHERE user_id IS NULL OR user_id = ? ORDER BY routine_id DESC", (session["user_id"],))
        routine_history = cur.fetchall()

        return render_template("routine.html", 
        exercises=exercises, antirotations=ANTIROTATIONS, equipments=equipments, variations=variations, routine_history=routine_history)


@app.route("/history")
@login_required
def history():

    db = sqlite3.connect("workouts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Display all routines in database from SQLite on history.html
    cur.execute("SELECT * FROM routine WHERE user_id IS NULL OR user_id = ? ORDER BY routine_id DESC", (session["user_id"],))
    routines = cur.fetchall()

    return render_template("history.html", routines=routines)


@app.route("/timer")
def timer():

    return render_template("timer.html")


@app.route("/success")
@login_required
def success():

    return render_template("success.html")


@app.route("/data")
@login_required
def data():

    return render_template("data.html")


@app.route("/account")
@login_required
def account():

    return render_template("account.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (submitting a form to register an account)
    if request.method == "POST":

        # Set error to None
        error = None

        # Get data from registration form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username is submitted
        if not username:
            error = "Must enter a username"
            return render_template("register.html", error=error)

        # Ensure username is submitted
        if not email:
            error = "Must enter an email"
            return render_template("register.html", error=error)

        # Check if username and email are already in database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        
        # Check for username
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        username_match = cur.fetchone()

        # Check for email
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        email_match = cur.fetchone()
        db.close()

        if username_match is not None:
            error = "Username already in use"
            return render_template("register.html", error=error)

        if email_match is not None:
            error = "Email is already in use"
            return render_template("register.html", error=error)

        # Ensure password was submitted
        if not password:
            error = "Must provide password"
            return render_template("register.html", error=error)

        # Ensure password confirmation match
        if not password == confirmation:
            error = "Passwords do not match"
            return render_template("register.html", error=error)

        # Generate encrypted password
        hash = generate_password_hash(password)

        # Remember username, email and password
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute("INSERT INTO users (username, email, hash) VALUES (?,?,?)", (username, email, hash))
        db.commit()
        db.close()

        flash("You registered, which is great!  Sorry, but I haven't figured out how to register and automatically log in, so you'll need to login now.  I'll get better soon!")
        return redirect("/login")

    # User reached route via GET (as by clicking or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

             # Ensure username was submitted
        if not username:
            error = "Must enter username"
            return render_template("login.html", error=error)

        # Ensure password was submitted
        elif not password:
            error = "Must enter password"
            return render_template("login.html", error=error)

        else:
            # Query database for username
            db = sqlite3.connect("workouts.db")
            cur = db.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = cur.fetchall()

            # Ensure username exists
            if len(rows) != 1:
                error = "Incorrect username"
                return render_template("login.html", error=error)

            # Ensure password is correct
            if not check_password_hash(rows[0][2], password):
                error = "Password does not match with the username provided"
                return render_template("login.html", error=error)

            # Remember which user has logged in
            session["user_id"] = rows[0][0]
            session["username"] = rows[0][1]
            session["email"] = rows[0][3]

            print(session["user_id"])
            print(session["username"])
            print(session["email"])

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
