from flaskapp.models import User,  UserRoles, UserSubjects,  Role,  Subject, Question, Answer, Test, UserAnswers
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flaskapp.auth import token_required
from flaskapp import db, app, bcrypt

routes = Blueprint('routes', __name__)


@routes.route('/subjects/<string:username>', methods=['GET'])
@token_required
def getSubjects(current_user, username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': "this username doesn't exist"}), 400

    subjects = user.subjects
    return jsonify({'user_subjects': [subject.serialize() for subject in subjects]}), 200


@routes.route('/create-test', methods=['POST'])
@token_required
def createTest(current_user):
    data = request.get_json()

    author = data.get('author')
    subject_name = data.get('subject_name')
    test_name = data.get('test_name')
    questions = data.get('questions')

    user = User.query.filter_by(username=author).first()

    subject = Subject.query.filter_by(name=subject_name).first()

    if not user or not subject:
        return jsonify({'message': "user or subject is not exist"}), 400

    t = Test(name=test_name)

    for question in questions:
        q = Question(text=question['text'])
        for answer in question['answers']:
            a = Answer(is_true=answer['is_true'], text=answer['text'])
            db.session.add(a)
            q.answers.append(a)

        t.questions.append(q)
        db.session.add(q)

    user.tests.append(t)
    subject.tests.append(t)

    db.session.add(user)
    db.session.add(subject)
    db.session.add(t)

    db.session.commit()

    return jsonify({'message': "successful added test"}), 200


class TestDTO:
    def __init__(self, id, author, test_name):
        self.id = id
        self.author = author
        self.test_name = test_name

    def serialize(self):
        return {
            'id': self.id,
            'author': self.author,
            'test_name': self.test_name,
        }


@routes.route('/tests-list/<string:subject_name>', methods=['GET'])
@token_required
def getTestsBySubject(current_user, subject_name):

    subject = Subject.query.filter_by(name=subject_name).first()

    if not subject:
        return jsonify({'message': "subject doesn't exist"}), 400

    tests_list = []
    for test in subject.tests:
        user = User.query.filter_by(id=test.author_id).first()
        tests_list.append(TestDTO(test.id, user.username, test.name))

    return jsonify({'tests': [test.serialize() for test in tests_list]}), 200


@routes.route('/test/<string:test_name>', methods=['GET'])
@token_required
def getTestsByName(current_user, test_name):

    test = Test.query.filter_by(name=test_name).first()

    if not test:
        return jsonify({'message': "test doesn't exist"}), 400

    return jsonify({'test': test.serialize(False)}), 200


@routes.route('/finish-test', methods=['POST'])
@token_required
def finishTest(current_user):
    data = request.get_json()

    student_id = data.get('student_id')
    answers = data.get('answers')

    user = User.query.filter_by(id=student_id).first()

    if not user:
        return jsonify({'message': "student is not exist"}), 400

    for answer in answers:
        ua = UserAnswers(is_true=answer['is_true'])
        a = Answer.query.filter_by(id=answer['answer_id']).first()
        ua.answers = a
        user.answers.append(ua)
        a.users.append(ua)
        db.session.add(ua)
        db.session.add(a)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': "test finished"}), 200


@routes.route('/test-solution/<string:test_name>', methods=['GET'])
@token_required
def getTestSolution(current_user, test_name):

    test = Test.query.filter_by(name=test_name).first()

    if not test:
        return jsonify({'message': "test doesn't exist"}), 400

    return jsonify({'test': test.serialize(True)}), 200
   