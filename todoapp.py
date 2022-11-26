from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
import json
import os

app = Flask(__name__)
app.secret_key = 'jfakflafjakdjfaj;dfj;aj'

TASKS = []
if os.path.exists('tasks.txt'):
    with open('tasks.txt', 'r') as filehandler:
        TASKS.append(json.load(filehandler))
        TASKS = [item for sub_list in TASKS for item in sub_list]
    

@app.route("/", methods=["GET", "POST"])
def get_tasks():
    if request.method == 'POST':
        return render_template("index.html", tasks=TASKS)
    return render_template("index.html", tasks=TASKS)

@app.route("/submit", methods=["GET", "POST"])
def post_tasks():
    error = None
    if request.method == 'POST':
        task = request.form["task"]
        email = request.form["email"]
        if not task or not task.strip():
            error = "name can't be empty"
        if not email or not email.strip() or '@' not in email:
            error = "email is not in correct format, try again"
        if error:
            flash(error)
            return redirect(url_for('get_tasks'))
        else:
            TASKS.append({"task":request.form["task"], "email":request.form["email"], "priority":request.form["priority"]})
            return redirect(url_for('get_tasks'))
    return redirect(url_for('get_tasks'))

@app.route("/clear")
def clear_tasks():
    print(TASKS)
    TASKS.clear()
    if os.path.exists('tasks.txt'):
        os.remove('tasks.txt')
    return redirect(url_for('get_tasks'))

@app.route("/save")
def save_tasks():
    print(TASKS)
    with open("tasks.txt", "w") as filehandle:
        json.dump(TASKS, filehandle)
        flash("Tasks Saved")
    return redirect(url_for('get_tasks'))

@app.route("/delete/<task_num>")
def delete_one(task_num):
    TASKS.pop(int(task_num))
    flash("Don't forget to save")
    return render_template("index.html", title="Home", tasks=TASKS)