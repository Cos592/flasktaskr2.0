from views import db
from datetime import date
from models import Task, User
from views import bcrypt
#import os
#from flask_sqlalchemy import SQLAlchemy
#basedir = os.path.abspath(os.path.dirname(__file__))
#from models import User, Task
    
db.create_all()

db.session.add(User("admin", "admin@admin.admin", bcrypt.generate_password_hash("admin"), "admin"))
db.session.add(User("qwerty", "qwerty@gmail.gg", bcrypt.generate_password_hash("qwerty"), "user"))
db.session.commit()

