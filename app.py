# create a web app that can create and record workout routines
import sqlite3
from datetime import datetime
from flask import (Flask, redirect, render_template, request)

# Configure application
app = Flask(__name__)

# Connect SQLite to database
db = sqlite3.connect("workouts.db")

CHAINS = ["Anterior", "Posterior", "Compound"]
FOCUSES = ["Lower", "Middle", "Upper"]
ANTIROTATIONS = ["None", "Single Arm", "Single Leg", "Twist", "Pallof"]

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    db = sqlite3.connect("workouts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Display all routines in database from SQLite on history.html
    cur.execute("SELECT * FROM routine ORDER BY routine_id DESC LIMIT 4")
    routines = cur.fetchall()

    return render_template("index.html", routines=routines)


@app.route("/equipment", methods=["GET", "POST"])
def equipment():
    if request.method == "POST":

        # Add equipment to equipment database
        equipment = request.form.get("equipment")

        # Remember equipment to database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute(
            "INSERT INTO equipments (equipment) VALUES(?)", (equipment,))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/equipment")

    else:
        # Display all equipments in database from SQLite on equipment.html
        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM equipments ORDER BY equipment")
        equipments = cur.fetchall()

        return render_template("equipment.html", equipments=equipments)


@app.route("/exercises", methods=["GET", "POST"])
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
        cur.execute("INSERT INTO exercises (exercise, variation, focus, muscle, chain) VALUES(?,?,?,?,?)",
                    (exercise, variation, focus, muscle, chain))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/exercises")

    else:

        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()

        # Display all muscles in dropdown menu selection
        cur.execute("SELECT muscle FROM muscles")
        muscles = cur.fetchall()

        # Display all exercises in database from SQLite on exercises.html
        cur.execute("SELECT * FROM exercises")
        exercises = cur.fetchall()

        return render_template("exercises.html", exercises=exercises, muscles=muscles, chains=CHAINS, focuses=FOCUSES, antirotations=ANTIROTATIONS)


@app.route("/muscles", methods=["GET", "POST"])
def muscles():
    if request.method == "POST":

        # Add muscle to muscles database
        muscle = request.form.get("muscle")

        # Remember muscle to database
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()
        cur.execute("INSERT INTO muscles (muscle) VALUES(?)", (muscle,))

        # Commit changes and close connection
        db.commit()
        db.close()

        return redirect("/muscles")

    else:
        # Display all muscles in database from SQLite on muscles.html
        db = sqlite3.connect("workouts.db")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM muscles ORDER BY muscle")
        muscles = cur.fetchall()

        return render_template("muscles.html", muscles=muscles)


@app.route("/routine", methods=["GET", "POST"])
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
            cur.execute("INSERT INTO routine (date, time, exercise, variation, antirotation, equipment, sets, reps, weight, notes) VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (date, time, exercise, variation, antiroation, equipment, sets, reps, weight, notes))

            # Commit changes and close connection
            db.commit()
        db.close()

        return redirect("/success")

    else:

        # Connecting to SQLite
        db = sqlite3.connect("workouts.db")
        cur = db.cursor()

        # Get list of exercises for dropdown menu selection
        cur.execute("SELECT DISTINCT exercise FROM exercises ORDER BY exercise")
        exercises = cur.fetchall()

        # Get list of variations for each exercise and store as dictionary of tuples with tuples
        # e.g. 'Exercise': [(exercise_id1, variation1), (exercise_id2, variation2)]
        variations = {}
        for exercise in exercises:
            cur.execute(
                "SELECT exercise_id, variation FROM exercises WHERE exercise=? ORDER BY exercise, variation", (exercise[0],))
            temp = cur.fetchall()
            variations[exercise[0]] = temp

        # Display all equipment in dropdown menu selection
        cur.execute("SELECT equipment FROM equipments ORDER BY equipment")
        equipments = cur.fetchall()

        # Get routine history to provide placeholders with dynamic data in routine table setup
        # Provides list of tuple e.g.: [(exercise, variation, ..., notes), (exercise, varaition, ..., notes)]
        cur.execute(
            "SELECT exercise, variation, antirotation, equipment, sets, reps, weight, notes FROM routine ORDER BY routine_id DESC")
        routine_history = cur.fetchall()

        return render_template("routine.html", exercises=exercises, antirotations=ANTIROTATIONS, equipments=equipments, variations=variations, routine_history=routine_history)


@app.route("/history")
def history():

    db = sqlite3.connect("workouts.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Display all routines in database from SQLite on history.html
    cur.execute("SELECT * FROM routine ORDER BY routine_id DESC")
    routines = cur.fetchall()

    return render_template("history.html", routines=routines)


@app.route("/timer")
def timer():

    return render_template("timer.html")


@app.route("/success")
def success():

    return render_template("success.html")


@app.route("/data")
def data():

    return render_template("data.html")


if __name__ == "__main__":
    app.run(debug=True)
