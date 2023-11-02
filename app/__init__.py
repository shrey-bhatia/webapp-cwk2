# __author__ = 'Shrey Bhatia'
# __email__ = 'fy21sb@leeds.ac.uk'
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


__author__ = 'Shrey Bhatia'
__email__ = 'fy21sb@leeds.ac.uk'

db = SQLAlchemy()
DB_NAME = "my_database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseGiveMeMarks'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


from app import views
from app.models import Income, Expense, Goal

create_database(app)
