from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "my_database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseGiveMeMarks'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
from webapp import views

def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
