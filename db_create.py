from views import db
from datetime import date
from models import Task, User
#import os
#from flask_sqlalchemy import SQLAlchemy
#basedir = os.path.abspath(os.path.dirname(__file__))
#from models import User, Task
    
db.session.add(Task("dffdsdfdsfdsd", date(2022,11,23), 5, date(2022,11,8), 1, 2))
#db.session.add(Task("Finish this tutorial", date(2015, 3, 13), 10, date(2022, 4, 23), 1, 1))
#db.session.add(Task("Finish Real Python", date(2022, 10, 22), 4 , date(1999,3,30), 1, 1))
db.session.commit()

