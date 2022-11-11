
from flask_bcrypt import Bcrypt
from datetime import date, datetime
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, make_response
from forms import AddTaskForm, RegisterForm, LoginForm

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


#config

app=Flask(__name__)
app.config.from_pyfile("_config.py")
bcrypt=Bcrypt(app)
db = SQLAlchemy(app)

from models import Task, User

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))
    return wrap


#route handlers

@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    session.pop("useer_id", None)
    session.pop("user_role", None)
    session.pop("user_name", None)
    flash("Goodbye")
    return redirect(url_for("login"))

@app.route("/", methods=["GET","POST"])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method=="POST":
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form["name"]).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form["password"]):
                session["logged_in"] = True
                session['user_id'] = user.id
                session["user_role"] = user.role
                session["user_name"] = user.name
                flash("Welcome")
                return redirect(url_for("tasks"))
            else:
                error = "invalid username or password"
        else:
            error = "both fields are required"
    return render_template("login.html", form=form, error=error)

def open_tasks():
    if session["user_role"] == "admin":
        return db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())
    else:
        return db.session.query(Task).filter_by(status="1", user_id=session["user_id"]).order_by(Task.due_date.asc())


def closed_tasks():
    if session["user_role"] == "admin":
        return db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())
    else:
        return db.session.query(Task).filter_by(status="0", user_id=session["user_id"]).order_by(Task.due_date.asc())


@app.route("/tasks/")
@login_required
def tasks():
    return render_template("tasks.html", form=AddTaskForm(request.form), open_tasks=open_tasks(), closed_tasks=closed_tasks())


@app.route("/add/", methods=["POST"])
@login_required
def new_task():
    error=None
    form=AddTaskForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = Task(form.name.data,form.due_date.data, form.priority.data, datetime.utcnow(), 1, session["user_id"])
            db.session.add(new_task)
            db.session.commit()
            flash("Entry Added")
            return redirect(url_for("tasks"))
        else:
            return render_template("tasks.html", form=form, error=error, open_tasks=open_tasks(), closed_tasks=closed_tasks())
    return render_template("tasks.html", form=form, error=error)
    
@app.route("/complete/<int:task_id>")
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session["user_id"]== task.first().user_id or session["user_role"] == "admin":
        task.update({"status":0})
        db.session.commit()
        flash("Task marked as completed")
        return redirect(url_for("tasks"))
    else:
        flash("You can only update your own tasks.")
        return redirect(url_for("tasks"))
    
    
@app.route("/delete/<int:task_id>")
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session["user_id"]== task.first().user_id  or session["user_role"] == "admin":
        task.delete()
        db.session.commit()
        flash("the task was deleted")
        return redirect(url_for("tasks"))
    else:
        flash("You can only delete your own tasks.")
        return redirect(url_for("tasks"))

@app.route("/register/", methods=["GET","POST"])
def register():
    error= None
    form = RegisterForm(request.form)
    if request.method == "POST":
        print("passed POST")
        if form.validate_on_submit():
            print("passed validation")
            new_user = User(form.name.data, form.email.data,bcrypt.generate_password_hash(form.password.data), "user")
            try:
                print("entered try")
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering. Please Login")
                return redirect(url_for("login"))
            except IntegrityError:
                error = "Username or email already in use"
                return render_template("register.html", form=form, error=error)
        else:
            print("failed validation")
    return render_template("register.html",form=form, error=error)

@app.route("/api/v1/tasks/")
def api_tasks():
    results = db.session.query(Task).all()
    json_results=[]
    for results in results:
        data = {
            "task_id" : results.task_id,
            "task_name" : results.name,
            "due_date" : str(results.due_date),
            "priority" : results.priority,
            "posted_date" : str(results.posted_date),
            "status" : results.status,
            "user_id" : results.user_id
        }
        json_results.append(data)
    return jsonify(items=json_results)

@app.route("/api/v1/tasks/<int:task_id>")
def api_tasks_single(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        json_result={
            "task_id" : result.task_id,
            "task_name" : result.name,
            "due_date" : str(result.due_date),
            "priority" : result.priority,
            "posted_date" : str(result.posted_date),
            "status" : result.status,
            "user_id" : result.user_id
        }
        code = 200
    else:
        code = 404
        json_result = {"error": "element does not exist"}
    return make_response(jsonify(json_result), code)

    
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"error in the %s field - %s" % (getattr(form, field).label.text, error), "error")
            
    
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

