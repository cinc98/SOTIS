from flaskapp.models import User, Subject, Answer, Question, TestQuestions, Test
from flaskapp import db
from flask import jsonify


def getUsers():
    return jsonify({'users': [u.serialize() for u in User.query.all()]}), 200


def addSubjectsToUser(user_subjects):

    user_subjects = user_subjects.get('user_subjects')

    for us in user_subjects:
        user = User.query.filter_by(id=us['user_id']).first()
        user.subjects = []

        for subject in us['subjects']:
            s = Subject.query.filter_by(id=subject['id']).first()
            if s not in user.subjects:
                user.subjects.append(s)
            db.session.add(user)

    db.session.commit()

    return jsonify({'message': "successfully added subjects to user"}), 200

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



def getStudentTests(student):

    student_answers = student.answers 


    questions = []

    for sa in student_answers:
         a = Answer.query.filter_by(id=sa.answer_id).first()
         if a.question_id not in questions:
            questions.append(a.question_id)

    tests=[]
    for q in questions:
        question = TestQuestions.query.filter_by(question_id=q).first()
        test = Test.query.filter_by(id=question.test_id).first()
        user = User.query.filter_by(id=test.author_id).first()
        test_dto = TestDTO(test.id, user.username, test.name).serialize()

        if test_dto not in tests:
            tests.append(test_dto)

    return jsonify({'tests': tests}), 200

def getStudentAnswers(student,test_name):

    test = Test.query.filter_by(name=test_name).first()

    questions = test.questions
    student_answers = student.answers 

    test_answers = {}

    for q in questions:
        for a in q.answers:
            for sa in student_answers:
                if sa.answer_id == a.id:
                    test_answers[a.id] = sa.is_true


    return jsonify({'answers': test_answers}), 200



