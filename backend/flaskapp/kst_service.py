import pandas as pd
import sys
from flaskapp import db, app, bcrypt
from flaskapp.models import *
from operator import itemgetter, attrgetter
from flask import jsonify
from itertools import combinations
from bunch import bunchify
import json

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


def is_question_correct(questions):

    q = Question.query.filter_by(id=questions[0]['id']).first()

    for i, a in enumerate(questions[0]['answers']):
        if 'is_true' not in a:
            if q.answers[i].is_true != False:
                return False
        else:
            if a['is_true'] != q.answers[i].is_true:
                return False

    return True


def calculate_probabilities(data, current_user):

    test = data.get('test')
    probabilities = data.get('probabilities')
    asked_questions = data.get('asked_questions')


    asked_questions.append(test['questions'])

    test1 = Test.query.filter_by(id=test['id']).first()
    questions = test1.questions

    ks = get_ks_by_test(test['name'])

    all_problems = [p for p in ks.problems]
    sorted_problems = sorted(all_problems, key=lambda i: i.weight)


    sorted_questions = []
    for sp in sorted_problems:
        sorted_questions.append(sp.questions[0])   

    node = [n for n in sorted_problems if n.title == test['questions'][0]['problem']['name']]

    problem = [1 if p.title == test['questions'][0]['problem']['name'] else 0 for p in sorted_problems]

    problem_index = problem.index(max(problem))



    if is_question_correct(test['questions']):

        for key, values in probabilities.items():
            if problem_index != None:
                if key[problem_index] == '1':

                    probabilities[key] = 1.5*values

                else:
                    probabilities[key] = values*0.5
    else:
         for key, values in probabilities.items():
            if problem_index != None:
                if key[problem_index] == '1':

                    probabilities[key] = 0.5*values

                else:
                    probabilities[key] = values*1.5
    
    

    most_common = max(probabilities , key=probabilities.get)
    

    ret_test = test1

    print(probabilities)

    print(most_common)
    print(float(probabilities[most_common]))
 
    if most_common == '00000':
        print("nista ne zna")
        state = UserStates()
        state.user_id = current_user.id
        state.test_id = test1.id
        state.state = most_common
        db.session.add(state)
        db.session.commit()
        return jsonify({'probabilities': probabilities}), 200


    else:
        if is_question_correct(test['questions']):

            nodes_above = get_nodes_above(node[0],ks)
            print(nodes_above)
            non_asked = non_asked_question(asked_questions, sorted_questions, nodes_above, most_common)

            if non_asked == None:
                print("nema pitanja")
                state = UserStates()
                state.user_id = current_user.id
                state.test_id = test1.id
                state.state = most_common
                db.session.add(state)
                db.session.commit()
                return jsonify({'probabilities': probabilities}), 200


            ret_test.questions = [non_asked]
            return jsonify({'probabilities': probabilities, 'asked_questions': asked_questions, 'test': ret_test.serialize(False)}), 200

        else:
            nodes_under = get_nodes_under(node[0],ks)

            non_asked = non_asked_question(asked_questions, sorted_questions, nodes_under, most_common)

            if non_asked == None:
                print("nema pitanja")
                state = UserStates()
                state.user_id = current_user.id
                state.test_id = test1.id
                state.state = most_common
                db.session.add(state)
                db.session.commit()
                return jsonify({'probabilities': probabilities}), 200


            ret_test.questions = [non_asked]
            return jsonify({'probabilities': probabilities, 'asked_questions': asked_questions, 'test': ret_test.serialize(False)}), 200



def non_asked_question(asked, sorted_questions, nodes, most_common):
    new_ask = []
    for a in asked:
        for sq in sorted_questions:
            if a[0]['id'] == sq.id:
                new_ask.append(sq)

    nodes = sorted(nodes, key=lambda i: i.weight)

    for n in nodes:
        if n.questions[0] not in new_ask:
            return n.questions[0]

    maks = max([i for i, ltr in enumerate(most_common) if ltr == '1'])
    contains = True
    while contains:
        if [i for i, ltr in enumerate(most_common) if ltr == '1'] != []:
            if sorted_questions[max([i for i, ltr in enumerate(most_common) if ltr == '1'])] in new_ask:
                new = list(most_common)
                new[max([i for i, ltr in enumerate(most_common) if ltr == '1'])] = '0'
                most_common = ''.join(new)
            else:
                return (sorted_questions[max([i for i, ltr in enumerate(most_common) if ltr == '1'])])
        else:
            for sq in sorted_questions:
                if sq not in new_ask:
                    return sq

            return None
            



def get_nodes_under(node, ks):

    nodes_under = []

    for l in ks.links:
        if l.target_id == node.id:
            for p in ks.problems:
                if p.id == l.source_id:
                    nodes_under.append(p)
                    nodes_under += get_nodes_under(p, ks)

    return nodes_under


def get_nodes_above(node, ks):

    nodes_above = []

    for l in ks.links:
        if l.source_id == node.id:
            for p in ks.problems:
                if p.id == l.target_id:
                    nodes_above.append(p)
                    nodes_above += get_nodes_above(p, ks)

    return nodes_above


def get_first_question(test_name):

    test = Test.query.filter_by(name=test_name).first()
    questions = test.questions

    asked_questions = []

    stanja_znanja = {}
    stanja_znanja['00000'] = 0
    ks = get_ks_by_test(test_name)
    ks_states = generate_knowledge_states(test_name)

    for k in ks_states:
        stanja_znanja[k] = 0

    all_problems = [p for p in ks.problems]
    sorted_problems = sorted(all_problems, key=lambda i: i.weight)

    sorted_questions = []
    for sp in sorted_problems:
        sorted_questions.append(sp.questions[0])

    # students_answers = get_matrix(test_name)

    students_answers = get_dict_from_pisa()

    broj_studenata = 0

    for key, values in students_answers.items():
        if ''.join(map(str, values)) in stanja_znanja:
            stanja_znanja[''.join(map(str, values))] += 1
            broj_studenata += 1

    for key, values in stanja_znanja.items():
        stanja_znanja[key] = values/broj_studenata

    most_common = max(stanja_znanja, key=stanja_znanja.get)
    ret_test = test

    if most_common == '00000':
        ret_test.questions = [sorted_questions[0]]
        return jsonify({'probabilities': stanja_znanja, 'asked_questions': asked_questions,'test': ret_test.serialize(False)}), 200

    else:
        ret_test.questions = [sorted_questions[max([i for i, ltr in enumerate(most_common) if ltr == '1'])]]
        return jsonify({'probabilities': stanja_znanja, 'asked_questions': asked_questions, 'test': ret_test.serialize(False)}), 200


def get_dict_from_pisa():

    students_answers = {}

    with open('./pisa.txt') as f:
        lines = f.readlines()
        for line in lines[1:]:
            students_answers[line[0:4].strip()] = [int(i)
                                                   for i in line[4:len(line)].strip('\n').split(' ')]

    return students_answers


def generate_knowledge_states(test_name):

    ks = get_ks_by_test(test_name)

    all_problems = [p for p in ks.problems]
    sorted_problems = sorted(all_problems, key=lambda i: i.weight)

    start_problem = sorted_problems[0]
    len_problems = len(all_problems)

    matrix = []

    matrix.append("1" + "0" * (len_problems - 1))

    curr_lst = ["0" for i in range(len_problems)]
    curr_lst[0] = "1"

    matrix = get_states(sorted_problems, start_problem,
                        matrix, len_problems, curr_lst)


    for bc in list(combinations(matrix, 2)):
        # print( str(int(bc[0], base=2)) + " + " + str(int(bc[1], base=2)) + " = " + str(int(bc[0], base=2) | int(bc[1], base=2)))
        # print(str(bin(int(bc[0], base=2) | int(bc[1], base=2))).split('b')[1])
        if str(bin(int(bc[0], base=2) | int(bc[1], base=2))).split('b')[1] not in matrix:
            matrix.append(
                str(bin(int(bc[0], base=2) | int(bc[1], base=2))).split('b')[1])


    return matrix


def get_states(all_problems, start_problem, matrix, len_problems, curr_lst, visited_problems=[]):
    visited_problems.append(start_problem)
    pr_ats = get_links(start_problem)
    temp_curr_lst = curr_lst.copy()
    if len(pr_ats) > 0:
        for p_a in pr_ats:
            pr = [pro for pro in all_problems if p_a.target_id == pro.id]
            temp_curr_lst[all_problems.index(pr[0])] = "1"
            curr_str = "".join(curr_lst)
            if curr_str not in matrix:
                matrix.append(curr_str)
            get_states(all_problems, pr[0], matrix,
                       len_problems, temp_curr_lst, visited_problems)
            temp_curr_lst = curr_lst.copy()
    else:
        temp_curr_lst[all_problems.index(start_problem)] = "1"
        curr_str = "".join(curr_lst)
        if curr_str not in matrix:
            matrix.append(curr_str)

    return matrix


def get_links(start_problem):
    ks = KnowledgeSpace.query.filter_by(
        id=start_problem.knowledge_space_id).first()
    links = []
    for l in ks.links:
        if l.source_id == start_problem.id:
            links.append(l)

    return links


def show_knowledge_states(test_name,student_name):

    test = Test.query.filter_by(name=test_name).first()
    user = User.query.filter_by(username=student_name).first()

    user_state = UserStates.query.filter_by(test_id=test.id).filter_by(user_id=user.id).first()

    ks = get_ks_by_test(test_name)

    new_ks = KnowledgeSpace()

    new_ks.title = ks.title + ' - All states'

    p = Problem()
    p.id= 0
    p.title='0'
    new_ks.problems.append(p)

    all_problems = [p for p in ks.problems]
    sorted_problems = sorted(all_problems, key=lambda i: i.weight)

    problems={}
    for i,s in enumerate(sorted_problems):
        problems[i]= s.title


    ks_states = generate_knowledge_states(test_name)


    for state in ks_states:
        state_indices = [i for i, ltr in enumerate(state) if ltr == '1']
        p = Problem()
        p.id = int(state, base=2)
        p.title=''
        if len(state_indices) == len(all_problems):
            p.id = int(state, base=2)
            p.title += 'Q'
            new_ks.problems.append(p)
        else:
            for si in state_indices:
                p.title += problems[si]+ ' '
                new_ks.problems.append(p)

    new_ks.links = generate_links(new_ks.problems)


    return jsonify({'knowledge_space': new_ks.serialize(), 'state': user_state.serialize()}), 200


def generate_links(states):
    links = []
    for s in states:
        binary_sid = bin(s.id).split('b')[1]
        num_of_nodes_source = binary_sid.count("1")
        for t in states:
            binary_tid = bin(t.id).split('b')[1]
            num_of_nodes_target = binary_tid.count("1")
            if num_of_nodes_target - num_of_nodes_source == 1:
                if one_bit_off(binary_sid, binary_tid):
                    l = Link()
                    l.source_id = s.id
                    l.target_id = t.id
                    links.append(l)

    return links

def one_bit_off(source, target):
    # print(str(bin(int(source, base=2) ^ int(target, base=2))).split('b')[1].count('1'))
    if str(bin(int(source, base=2) ^ int(target, base=2))).split('b')[1].count('1') == 1:
        return True
    else:
        return False