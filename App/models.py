
from .exts import db

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_number = db.Column(db.String(255), nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    book_type = db.Column(db.String(255), nullable=False)
    book_price = db.Column(db.Float, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    book_publisher = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

