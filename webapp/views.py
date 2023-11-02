from flask import render_template, request, url_for, redirect, flash
from webapp import app
from webapp.models import Income, Expense, Goal
from webapp import db


def floatcheck(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('homePage.html',
                           title='Home Page')


@app.route('/addGoalPage', methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        goalname = request.form.get('goalName')
        goalamount = request.form.get('goalAmount')
        # server side validation for goal name
        if len(goalname) > 50:
            flash('Goal name must be less than 50 characters.',
                  category='error')
        elif len(goalname) == 0:
            flash('Goal name must not be empty.', category='error')
        else:
            pass
        # server side validation for goal amount
        if floatcheck(goalamount):
            goalamount = round(float(goalamount), 2)
            if (goalamount >= 0.01) and (goalamount <= 999999.99):
                pass
            else:
                flash('Goal amount must be greater than 0.',
                      category='error')
        else:
            flash('Goal amount must be a number.', category='error')
        flash('Form submitted!', category='success')

    return render_template('addGoalPage.html',
                           title='Goal')


@app.route('/allExpensesPage')
def allexpensespage():
    return render_template('allExpensesPage.html',
                           title='All Expenses')


@app.route('/addIncomePage', methods=['GET', 'POST'])
def addincomepage():
    if request.method == 'POST':
        incometitle = request.form.get('incomeTitle')
        incomeamount = request.form.get('incomeAmount')
        # server side validation for income title
        if len(incometitle) > 50:
            flash('Income title must be less than 50 characters.',
                  category='error')
        elif len(incometitle) == 0:
            flash('Income title must not be empty.', category='error')
        else:
            pass
        # server side validation for income amount
        if floatcheck(incomeamount):
            incomeamount = round(float(incomeamount), 2)
            if (incomeamount >= 0.01) and (incomeamount <= 999999.99):
                pass
            else:
                flash('Income amount must be greater than 0.',
                      category='error')
        else:
            flash('Income amount must be a number.', category='error')
        # Check if an income with the same title already exists
        existing_income = Income.query.filter_by(title=incometitle).first()

        if existing_income is None:
            # If no existing income found, add the new income to the database
            new_income = Income(title=incometitle, amount=incomeamount)
            db.session.add(new_income)
            db.session.commit()
            flash('Income added!', category='success')
        else:
            flash('Income with this title already exists.', category='error')
        # flash('Form submitted!', category='success')

    return render_template('addIncomePage.html',
                           title='Add Income')


@app.route('/allIncomesPage')
def allincomespage():
    # Query all income records from the database
    all_incomes = Income.query.all()

    # Calculate the total income
    total = 0
    for income in all_incomes:
        total += income.amount

    return render_template('allIncomesPage.html',
                           title='All Incomes',
                           incomes=all_incomes,
                           total=total)

@app.route('/addExpensePage', methods=['GET', 'POST'])
def addexpensepage():
    if request.method == 'POST':
        expensentitle = request.form.get('expenseTitle')
        expenseamount = request.form.get('expenseAmount')
        # server side validation for expense title
        if len(expensentitle) > 50:
            flash('Expense title must be less than 50 characters.',
                  category='error')
        elif len(expensentitle) == 0:
            flash('Expense title must not be empty.', category='error')
        else:
            pass
        # server side validation for expense amount
        if floatcheck(expenseamount):
            expenseamount = round(float(expenseamount), 2)
            if (expenseamount >= 0.01) and (expenseamount <= 999999.99):
                pass
            else:
                flash('Expense amount must be greater than 0.',
                      category='error')
        else:
            flash('Expense amount must be a number.', category='error')
        flash('Form submitted!', category='success')

    return render_template('addExpensePage.html',
                           title='Add Expenses')
