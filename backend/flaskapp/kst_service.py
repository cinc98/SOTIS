import pandas as pd
import sys
from flaskapp import db, app, bcrypt
from flaskapp.models import *
from operator import itemgetter, attrgetter
from flask import jsonify

sys.path.append('learning_spaces/')
from learning_spaces.kst import iita


def create_real_ks(test_name):
    student_questions = pd.DataFrame(get_matrix(test_name))
    response = iita(student_questions, v=1)
    expected_ks = get_ks_by_test(test_name)

    ks = KnowledgeSpace.query.filter_by(
        title=expected_ks.title + " - Real").first()

    if ks:
        return jsonify({'message': "real ks for this test already exists"}), 200

    real_ks = KnowledgeSpace(title=expected_ks.title + " - Real",
                             domain_id=expected_ks.domain_id, is_real=True)

    for p in expected_ks.problems:
        new_problem = Problem(title=p.title, weight=p.weight)
        real_ks.problems.append(new_problem)

    db.session.add(real_ks)
    db.session.commit()

    saved_realks = KnowledgeSpace.query.filter_by(title=real_ks.title).first()

    for link in response['implications']:
        source = Problem.query.filter_by(knowledge_space_id=saved_realks.id).filter_by(
            title=saved_realks.problems[link[0]].title).first()
        target = Problem.query.filter_by(knowledge_space_id=saved_realks.id).filter_by(
            title=saved_realks.problems[link[1]].title).first()
        link = Link(source_id=source.id, target_id=target.id)
        saved_realks.links.append(link)
        db.session.add(link)

    db.session.add(real_ks)
    db.session.commit()

    return jsonify({'message': "successfully created real ks"}), 200


def get_ks_by_test(test_name):
    test = Test.query.filter_by(name=test_name).first()

    questions = test.questions
    for q in questions:
        return KnowledgeSpace.query.filter_by(id=q.problem.knowledge_space_id).filter_by(is_real=False).first()


def get_matrix(test_name):

    test = Test.query.filter_by(name=test_name).first()
    questions = test.questions

    students_answers = {}
    for q in questions:
        for a in q.answers:
            user_answers = UserAnswers.query.filter_by(answer_id=a.id).all()
            for ua in user_answers:
                if ua.user_id in students_answers:
                    students_answers[ua.user_id].append(
                        is_answer_correct(ua))
                else:
                    students_answers[ua.user_id] = [
                        is_answer_correct(ua)]

    student_results = {}
    student_results = dict.fromkeys(students_answers.keys())

    for key, value in students_answers.items():
        student_results[key] = get_list_question_iscorrect(
            sorted(value, key=lambda i: i['question_id'].problem.weight))

    print(student_results)

    return student_results


def is_answer_correct(user_answers):
    question = Question.query.filter_by(id=user_answers.answer.question_id
                                        ).first()

    if user_answers.answer.is_true == user_answers.is_true:
        return {'question_id': question, 'answer_id': user_answers.answer.id, 'correct': True}
    else:
        return {'question_id': question, 'answer_id': user_answers.answer.id, 'correct': False}


def get_list_question_iscorrect(dic):
    idfDict = {}
    for dicv in dic:
        if dicv['question_id'] in idfDict:
            idfDict[dicv['question_id']].append(dicv['correct'])
        else:
            idfDict[dicv['question_id']] = [dicv['correct']]

    question_correct = []
    for key, value in idfDict.items():
        if False in value:
            question_correct.append(0)
        else:
            question_correct.append(1)

    return question_correct
