from flask import render_template
from app import app


@app.route('/')
def home():
    user = {'name': 'Sam Wilson'}
    return render_template('homePage.html',
                           title='Home Page',
                           user=user)


@app.route('/addGoalPage')
def goal():
    return render_template('addGoalPage.html',
                           title='Goal')


@app.route('/allExpensesPage')
def allexpensespage():
    return render_template('allExpensesPage.html',
                           title='All Expenses')


@app.route('/addIncomePage')
def addincomepage():
    return render_template('addIncomePage.html',
                           title='Add Income')


@app.route('/allIncomesPage')
def allincomespage():
    return render_template('/allIncomesPage.html',
                           title='All Incomes')


@app.route('/addExpensePage')
def addexpensepage():
    return render_template('addExpensePage.html',
                           title='Add Expenses')
