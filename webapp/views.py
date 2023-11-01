from flask import render_template, request, url_for, redirect, flash
from webapp import app


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('homePage.html',
                           title='Home Page')


@app.route('/addGoalPage', methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        goalname = request.form.get('goalName')
        goalamount = request.form.get('goalAmount')
        #server side validation for goal name must be less than 50 characters
        if len(goalname) > 50:
            flash('Goal name must be less than 50 characters.',
                  category='error')
        elif len(goalname) == 0:
            flash('Goal name must not be empty.', category='error')
        else:
            pass
        #server side validation for goal amount
        if goalamount.isnumeric():
            goalamount = int(goalamount)
            if goalamount >= 0.01:
                flash('Form submitted!', category='success')
            else:
                flash('Goal amount must be greater than 0.',
                      category='error')
        else:
            flash('Goal amount must be a number.', category='error')
        flash('Form submitted!', category='success')
    else:
        flash('Goal does not exist.', category='error')

    return render_template('addGoalPage.html',
                           title='Goal')


@app.route('/allExpensesPage')
def allexpensespage():
    return render_template('allExpensesPage.html',
                           title='All Expenses')


@app.route('/addIncomePage', methods=['GET', 'POST'])
def addincomepage():
    return render_template('addIncomePage.html',
                           title='Add Income')


@app.route('/allIncomesPage')
def allincomespage():
    return render_template('allIncomesPage.html',
                           title='All Incomes')


@app.route('/addExpensePage', methods=['GET', 'POST'])
def addexpensepage():
    return render_template('addExpensePage.html',
                           title='Add Expenses')
