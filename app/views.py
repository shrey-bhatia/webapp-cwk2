from flask import render_template
from app import app


@app.route('/')
def home():
    user = {'name': 'Sam Wilson'}
    return render_template('base.html',
                           title='Home page',
                           user=user)


@app.route('/addGoalPage')
def goal():
    return render_template('base.html',
                           title='addGoalPage')


@app.route('/allExpensesPage')
def allexpensespage():
    return render_template('base.html',
                           title='allExpensesPage')


@app.route('/addIncomePage')
def addincomepage():
    return render_template('base.html',
                           title='addIncomePage')


@app.route('/allIncomesPage')
def allincomespage():
    return render_template('/base.html',
                           title='allIncomesPage')


@app.route('/addExpensePage')
def addexpensepage():
    return render_template('base.html',
                           title='addExpensePage')
