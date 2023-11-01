from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "my_database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseGiveMeMarks'
from webapp import views
