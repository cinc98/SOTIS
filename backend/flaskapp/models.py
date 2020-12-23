from datetime import datetime
from flaskapp import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    answers = db.relationship("UserAnswers", back_populates="user")

    subjects = db.relationship(
        'Subject', secondary='user_subjects', backref=db.backref('users', lazy='dynamic'))
    tests = db.relationship('Test', backref='user',
                            lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': [role.serialize() for role in self.roles],
            'subjects': [subject.serialize() for subject in self.subjects],
        }


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    domain_id = db.Column(db.Integer(), db.ForeignKey('domain.id'))
    domain = db.relationship('Domain', back_populates="subject")

    tests = db.relationship('Test', backref='subject',
                            lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'domain': self.domain.serialize() if self.domain != None else ''
        }


class UserSubjects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.Integer(), db.ForeignKey(
        'subject.id', ondelete='CASCADE'))


class Test(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    questions = db.relationship(
        'Question', secondary='test_questions', backref=db.backref('tests', lazy='dynamic'))
    subject_id = db.Column(db.Integer(), db.ForeignKey(
        'subject.id', ondelete='CASCADE'))
    author_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))

    def serialize(self, show_correct_answers):
        return {
            'id': self.id,
            'name': self.name,
            'author_id': self.author_id,
            'subject_id': self.subject_id,

            'questions': [question.serialize(show_correct_answers) for question in self.questions],
        }


class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    answers = db.relationship('Answer', backref='question',
                              lazy='dynamic')

    def serialize(self, show_correct_answers):
        return {
            'id': self.id,
            'text': self.text,
            'answers': [answer.serialize(show_correct_answers) for answer in self.answers],
            'problem': self.problem.serialize()
        }


class TestQuestions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    test_id = db.Column(db.Integer(), db.ForeignKey(
        'test.id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer(), db.ForeignKey(
        'question.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            'id': self.id,
            'test_id': self.test_id,
            'question_id': self.question_id

        }


class Answer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_true = db.Column(db.Boolean(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    users = db.relationship("UserAnswers", back_populates="answer")

    def serialize(self, show_correct_answers):
        if show_correct_answers:
            return {
                'id': self.id,
                'text': self.text,
                'is_true': self.is_true,
                'question_id': self.question_id
            }
        else:
            return {
                'id': self.id,
                'text': self.text,
                'question_id': self.question_id

            }


class Problem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    knowledge_space_id = db.Column(
        db.Integer, db.ForeignKey('knowledge_space.id'))
    questions = db.relationship('Question', backref='problem',
                                lazy='dynamic')
    weight = db.Column(db.Integer(), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.title,
            'weight': self.weight

        }


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    target_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    knowledge_space_id = db.Column(
        db.Integer, db.ForeignKey('knowledge_space.id'))

    def serialize(self):
        return {
            'sid': self.source_id,
            'tid': self.target_id,

        }


class KnowledgeSpace(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    is_real = db.Column(db.Boolean(), nullable=False)
    domain_id = db.Column(db.Integer(), db.ForeignKey(
        'domain.id', ondelete='CASCADE'))
    problems = db.relationship('Problem', backref='knowledge_space',
                               lazy='dynamic')
    links = db.relationship('Link', backref='knowledge_space',
                            lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'problems': [problem.serialize() for problem in self.problems],
            'links': [link.serialize() for link in self.links],
            'is_real': self.is_real

        }


class Domain(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    knowledge_spaces = db.relationship('KnowledgeSpace', backref='domain',
                                       lazy='dynamic')
    subject = db.relationship(
        'Subject', uselist=False, back_populates="domain", )

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }


class UserAnswers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    answer_id = db.Column(db.Integer(), db.ForeignKey(
        'answer.id', ondelete='CASCADE'))
    is_true = db.Column(db.Boolean(), nullable=False)
    answer = db.relationship("Answer", back_populates="users")
    user = db.relationship("User", back_populates="answers")

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user_id,
            'answer': self.answer.serialize(True),
            'student_answer': self.is_true
        }
