from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweasd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
bcrypt: Bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

db = SQLAlchemy(app)
