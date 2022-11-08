from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddTaskForm(FlaskForm):
    task_id = IntegerField()
    name = StringField("Task Name", validators=[DataRequired()])
    due_date = DateField("Date Due (dd/mm/yyyy)", validators=[DataRequired()])
    priority = SelectField("Priority", validators=[DataRequired()], choices=[("1", "1"), ("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10")])
    status = IntegerField("Status")
    
    
class RegisterForm(FlaskForm):
    name = StringField("username", validators=[DataRequired(), Length(min=6, max=38)])
    email = StringField("email", validators=[DataRequired(), Email(), Length(min=6, max=60)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    
class LoginForm(FlaskForm):
    name = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    