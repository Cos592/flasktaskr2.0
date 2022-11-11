import os
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "flasktaskr.db"
WTF_CSRF_ENABLED = True
DEBUG = True
SECRET_KEY = "9dksfldjldmsklnvkdlkldslfenklneiowfnoewno34n25328583425y4829f"
DATABASE_PATH = basedir+"/"+DATABASE
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH  
SQLALCHEMY_TRACK_MODIFICATIONS = False