from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Association table
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_isbn', db.String, db.ForeignKey('mytable.ISBN'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    likes = db.relationship('Book', secondary=likes, backref=db.backref('likers', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def has_liked(self, book):
        return any(like.ISBN == book.ISBN for like in self.likes)

class Book(db.Model):
    __tablename__ = 'mytable'
    ISBN = db.Column(db.String, primary_key=True)
    BookTitle = db.Column(db.String)
    BookAuthor = db.Column(db.String)
    YearOfPublication = db.Column(db.Integer)
    Publisher = db.Column(db.String)
    ImageURLS = db.Column(db.String)
    ImageURLM = db.Column(db.String)
    ImageURLL = db.Column(db.String)
    Price = db.Column(db.Float)
    like_count = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_isbn = db.Column(db.String, db.ForeignKey('mytable.ISBN'))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=1)  # Add this line
    book = db.relationship('Book', backref='carts')
