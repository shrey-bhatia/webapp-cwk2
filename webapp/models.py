from . import db

# Create a class for the table in the database for income
class Income(db.Model):
    title = db.Column(db.String(50),  primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Income('{self.title}', '{self.amount}')"

# Create a class for the table in the database for expenses
class Expense(db.Model):
    title = db.Column(db.String(50),  primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Expense('{self.title}', '{self.amount}')"

# Create a class for the table in the database for goals
class Goal(db.Model):
    name = db.Column(db.String(50),  primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Goal('{self.name}', '{self.amount}')"
