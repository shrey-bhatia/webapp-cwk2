# __author__ = 'Shrey Bhatia'
# __email__ = 'fy21sb@leeds.ac.uk'
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

__author__ = 'Shrey Bhatia'
__email__ = 'fy21sb@leeds.ac.uk'

db = SQLAlchemy()
DB_NAME = "booksdatabase.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseGiveMeMarks'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'userloginpage'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')


from app import views
from app.models import Book, User

create_database(app)
