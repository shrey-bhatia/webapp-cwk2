# __author__ = 'Shrey Bhatia'
# __email__ = 'fy21sb@leeds.ac.uk'
from flask import render_template, request, flash, redirect, url_for
from webapp import app
from webapp.models import Income, Expense, Goal
from webapp import db


def floatcheck(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def goal_form():
    if request.method == 'POST':
        if Goal.query.first() is not None:
            # delete old goal from database
            existing_goal = Goal.query.first()
            db.session.delete(existing_goal)
            db.session.commit()
        goalname = request.form.get('goalName')
        goalamount = request.form.get('goalAmount')
        # server side validation for goal name
        if len(goalname) > 50:
            flash('Goal name must be less than 50 characters.',
                  category='error')
        elif len(goalname) == 0:
            flash('You are adding a goal without a name.', category='error')
        else:
            pass
        # server side validation for goal amount
        if floatcheck(goalamount):
            goalamount = round(float(goalamount), 2)
            if (goalamount >= 0.01) and (goalamount <= 999999.99):
                # Create a new Goal instance and add it to the database
                new_goal = Goal(name=goalname, amount=goalamount)
                db.session.add(new_goal)
                db.session.commit()
                flash('Goal added!', category='success')
            else:
                flash('Goal amount must be greater than 0.',
                      category='error')
        else:
            flash('Goal amount must be a number.', category='error')
        flash('Form submitted!', category='success')


@app.route('/', methods=['GET', 'POST'])
def home():
    mywidth = 0
    if Goal:
        mygoal = Goal.query.first()
    # Calculate the total expense
    all_expenses = Expense.query.all()
    totalexp = 0
    for expense in all_expenses:
        totalexp += expense.amount

    # Calculate the total income
    all_incomes = Income.query.all()
    totalinc = 0
    for income in all_incomes:
        totalinc += income.amount

    balance = totalinc - totalexp
    balance = round(balance, 2)
    if mygoal is not None:
        if (mygoal.amount is not None) and (
                mygoal.amount != 0) and 0 <= balance <= mygoal.amount:
            mywidth = (balance / mygoal.amount * 100)
            mywidth = round(mywidth, 2)
        elif balance >= mygoal.amount:
            mywidth = 100
    else:
        mywidth = 0

    # delete goal button
    if request.method == 'POST':
        # delete old goal from database
        existing_goal = Goal.query.first()
        db.session.delete(existing_goal)
        db.session.commit()
        flash('Goal deleted!', category='success')
        return redirect(url_for('home'))

    return render_template('homePage.html',
                           title='Home Page', mywidth=mywidth, my_goal=mygoal,
                           totalexp=totalexp, totalinc=totalinc,
                           balance=balance)


@app.route('/addGoalPage', methods=['GET', 'POST'])
def goalpage():
    # Check if any goal exists in the database

    existing_goal = Goal.query.first()

    if existing_goal is None:
        goal_form()
        return render_template('addGoalPage.html',
                               title='Add Goal')
    else:
        # write code to edit goal instead of adding a new one
        # first confirm if user wants to edit goal
        # delete old goal from database
        # then add new goal
        goal_form()

        return render_template('addGoalPage.html',
                               title='Edit Goal')


@app.route('/allExpensesPage')
def allexpensespage():
    # Query all expense records from the database
    all_expenses = Expense.query.all()

    # Calculate the total expense
    total = 0
    expitems = []
    for expense in all_expenses:
        total += expense.amount
        expitems.append(expense)
    total = round(total, 2)

    return render_template('allExpensesPage.html',
                           title='All Expenses',
                           expenses=all_expenses,
                           total=total, expitems=expitems)


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
    incitems = []
    for income in all_incomes:
        total += income.amount
        incitems.append(income)
    total = round(total, 2)

    return render_template('allIncomesPage.html',
                           title='All Incomes',
                           incomes=all_incomes,
                           total=total, incitems=incitems)


@app.route('/addExpensePage', methods=['GET', 'POST'])
def addexpensepage():
    if request.method == 'POST':
        expensetitle = request.form.get('expenseTitle')
        expenseamount = request.form.get('expenseAmount')
        # server side validation for expense title
        if len(expensetitle) > 50:
            flash('Expense title must be less than 50 characters.',
                  category='error')
        elif len(expensetitle) == 0:
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
        # Check if an expense with the same title already exists
        existing_expense = Expense.query.filter_by(title=expensetitle).first()

        if existing_expense is None:
            # If no existing expense found, add the new expense to the database
            new_expense = Expense(title=expensetitle, amount=expenseamount)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', category='success')
        else:
            flash('Expense with this title already exists.', category='error')
        # flash('Form submitted!', category='success')

    return render_template('addExpensePage.html',
                           title='Add Expense')


@app.route('/expenseDelete/', methods=['GET', 'POST'])
def expense_delete():
    if request.method == 'POST' and request.form.get(
            'expenseToDel') is not None:
        # Get the expense title from the form
        expensetitledel = request.form.get('expenseToDel')
        print(expensetitledel)
        # Query the expense record from the database
        existing_expense = Expense.query.filter_by(
            title=expensetitledel).first()
        if existing_expense is None:
            flash('Expense not found.', category='error')
        else:
            # Delete the expense record from the database
            print("really deleting")
            db.session.delete(existing_expense)
            db.session.commit()
            flash('Expense deleted!', category='success')

    return redirect(url_for('allexpensespage'))


@app.route('/expenseEdit/', methods=['GET', 'POST'])
def expense_edit():
    if request.method == 'POST' and request.form.get(
            'expenseTitle') is not None:
        # Get the expense title from the form
        expensetitle = request.form.get('expenseTitle')
        try:
            expenseamount = float(request.form.get('expenseAmount'))
        except TypeError or ValueError:
            flash('Expense amount must be a number.', category='error')
            return redirect(url_for('allexpensespage'))
        # Query the expense record from the database
        existing_expense = Expense.query.filter_by(title=expensetitle).first()
        if existing_expense is None:
            flash('Expense not found.', category='error')
        else:
            # Validate the new expense amount

            if (expenseamount >= 0.01) and (
                    expenseamount <= 999999.99) and floatcheck(expenseamount):
                existing_expense.amount = expenseamount
                db.session.commit()
                flash('Expense edited!', category='success')
            else:
                flash('Invalid expense amount.',
                      category='error')

    return redirect(url_for('allexpensespage'))


@app.route('/incomeDelete/', methods=['GET', 'POST'])
def income_delete():
    if request.method == 'POST' and request.form.get(
            'incomeToDel') is not None:
        # Get the income title from the form
        incometitledel = request.form.get('incomeToDel')
        print(incometitledel)
        # Query the income record from the database
        existing_income = Income.query.filter_by(title=incometitledel).first()
        if existing_income is None:
            flash('Income not found.', category='error')
        else:
            # Delete the income record from the database
            print("really deleting")
            db.session.delete(existing_income)
            db.session.commit()
            flash('Income deleted!', category='success')

    return redirect(url_for('allincomespage'))


@app.route('/incomeEdit/', methods=['GET', 'POST'])
def income_edit():
    if request.method == 'POST' and request.form.get(
            'incomeTitle') is not None:
        # Get the income title from the form
        incometitle = request.form.get('incomeTitle')
        try:
            incomeamount = float(request.form.get('incomeAmount'))
        except TypeError or ValueError:
            flash('Income amount must be a number.', category='error')
            return redirect(url_for('allincomespage'))
        # Query the income record from the database
        existing_income = Income.query.filter_by(title=incometitle).first()
        if existing_income is None:
            flash('Income not found.', category='error')
        else:
            # Validate the new income amount

            if (incomeamount >= 0.01) and (
                    incomeamount <= 999999.99) and floatcheck(incomeamount):
                existing_income.amount = incomeamount
                db.session.commit()
                flash('Income edited!', category='success')
            else:
                flash('Invalid income amount.',
                      category='error')

    return redirect(url_for('allincomespage'))
