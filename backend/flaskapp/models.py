from datetime import datetime
from flaskapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    subjects = db.relationship('Subject', secondary='user_subjects', backref=db.backref('users', lazy='dynamic'))
    tests = db.relationship('Test', secondary='user_tests', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10), nullable=False)

class UserSubjects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id', ondelete='CASCADE'))

class Test(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_tests', backref=db.backref('tests', lazy='dynamic'))
    questions = db.relationship('Question', secondary='user_tests', backref=db.backref('tests', lazy='dynamic'))

class UserTests(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    test_id = db.Column(db.Integer(), db.ForeignKey('test.id', ondelete='CASCADE'))

class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    answers = db.relationship('Answer', secondary='question_answers', backref=db.backref('question', lazy='dynamic'))

class TestQuestions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    test_id = db.Column(db.Integer(), db.ForeignKey('test.id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id', ondelete='CASCADE'))

class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_true = db.Column(db.Boolean(), nullable=False)

class QuestionAnswers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    answer_id = db.Column(db.Integer(), db.ForeignKey('answer.id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id', ondelete='CASCADE'))

class UserAnswers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    answer_id = db.Column(db.Integer(), db.ForeignKey('answer.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    user_answer = db.Column(db.Boolean(), nullable=False)

