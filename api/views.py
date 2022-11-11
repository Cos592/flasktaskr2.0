from functools import wraps
from flask import flash, redirect, jsonify, session, url_for, Blueprint

from views import db
from models import Task

api_blueprint = Blueprint("api", __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))
    return wrap


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
    
    
@api_blueprint.route("api/v1/tasks/")
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results=[]
    for results in results:
        data = {
            "task_id" : results.task_id,
            "task_name" : results.task_name,
            "due_date" : str(results.due_date),
            "priority" : results.priority,
            "posted_date" : str(results.posted_date),
            "status" : results.status,
            "user_id" : results.user_id
        }
    json_results.append(data)
    return jsonify(items=json_results)
