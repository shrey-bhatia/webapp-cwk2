from . import db

# Create a class for the table in the database for income
class Income(db.Model):
    title = db.Column(db.String(50),  primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Income('{self.title}', '{self.amount}')"
