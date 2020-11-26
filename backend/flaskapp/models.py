from datetime import datetime
from flaskapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Test_question(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)