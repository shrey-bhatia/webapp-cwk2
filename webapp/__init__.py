from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pleaseGiveMeMarks'
from webapp import views
