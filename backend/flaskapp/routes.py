import xml.etree.cElementTree as ET
from flaskapp.models import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, send_file
from flaskapp.auth import token_required
from flaskapp import db, app, bcrypt
from flaskapp import kst_service
import zipfile
from io import BytesIO

routes = Blueprint('routes', __name__)


@routes.route('/get-realks/<string:test_name>', methods=['GET'])
def get_realks(test_name):

    return kst_service.create_real_ks(test_name)


@routes.route('/all-states/<string:test_name>', methods=['GET'])
def all_states(test_name):
    
    return kst_service.show_knowledge_states(test_name)

@routes.route('/test/first-question/<string:test_name>', methods=['GET'])
def get_test_first_question(test_name):
    
    return kst_service.get_first_question(test_name)


@routes.route('/ks-states/<string:test_name>', methods=['GET'])
def generate_knowledge_states(test_name):
    
    return kst_service.generate_knowledge_states(test_name)


@routes.route('/test/next-question', methods=['POST'])
def get_next_question():
    data = request.get_json()

    return kst_service.calculate_probabilities(data)

     


@routes.route('/get-xml/<string:test_name>', methods=['POST'])
def get_xml_file(test_name):

    test = Test.query.filter_by(name=test_name).first()
    data = BytesIO()

    with zipfile.ZipFile(data, 'w') as myzip:

        tree = ET.ElementTree()
        bio = BytesIO()

        root = ET.Element("qti-assessment-test")

        root.set("xmlns", "http://www.imsglobal.org/xsd/imsqtiasi_v3p0")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocatio", "http://www.imsglobal.org/xsd/imsqtiasi_v3p0 https://purl.imsglobal.org/spec/qti/v3p0/schema/xsd/imsqti_asiv3p0_v1p0.xsd")
        root.set("identifier", "TEST-" + str(test.id))
        root.set("title", test_name)

        test_part = ET.SubElement(root, "qti-test-part")
        test_part.set("navigation-mode", "linear")
        test_part.set("submission-mode", "individual")
        test_part.set("identifier", "Part 1")

        test_section = ET.SubElement(test_part, "qti-assessment-section")

        test_section.set("identifier", "set")
        test_section.set("title", "Section 1")
        test_section.set("visible", "true")

        test_selection = ET.SubElement(test_section, "qti-selection")
        test_selection.set("select", "2")

        for question in test.questions:
            question_item = ET.SubElement(
                test_selection, "qti-assessment-item-ref")
            question_item.set("identifier", str(question.id))
            question_item.set("href", "test" +
                              str(test.id) + "-" + str(question.id) + ".xml")

            tree1 = ET.ElementTree()
            bio1 = BytesIO()

            question_xml = ET.Element("qti-assessment-item")
            question_xml.set(
                "xmlns", "http://www.imsglobal.org/xsd/imsqtiasi_v3p0")
            question_xml.set(
                "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
            question_xml.set("xmlns:xi", "http://www.w3.org/2001/XInclude")
            question_xml.set(
                "xsi:schemaLocation", "http://www.imsglobal.org/xsd/imsqtiasi_v3p0 https://purl.imsglobal.org/spec/qti/v3p0/schema/xsd/imsqti_asiv3p0_v1p0.xsd")
            question_xml.set("identifier", "TEST-" +
                             str(test.id) + "-" + str(question.id))
            question_xml.set("title", "Question " + str(question.id))
            question_xml.set("adaptive", "false")
            question_xml.set("time-dependent", "false")
            question_response = ET.SubElement(
                question_xml, "qti-response-declaration")
            question_response.set("identifier", "RESPONSE")
            question_response.set("cardinality", "single")
            question_response.set("base-type", "identifier")
            question_correct_response = ET.SubElement(
                question_response, "qti-correct-response")
            question_response_value = ET.SubElement(
                question_correct_response, "qti-value")
            for answer in question.answers:
                if answer.is_true:
                    question_response_value.text = str(answer.id)

            question_out_decl = ET.SubElement(
                question_xml, "qti-outcome-declaration")
            question_out_decl.set("identifier", "SCORE")
            question_out_decl.set("cardinality", "single")
            question_out_decl.set("base-type", "float")
            question_body = ET.SubElement(question_xml, "qti-item-body")
            question_inter = ET.SubElement(
                question_body, "qti-choice-interaction")
            question_inter.set("response-identifier", "RESPONSE")
            question_inter.set("shuffle", "true")
            question_inter.set("max-choices", "1")
            question_prompt = ET.SubElement(question_inter, "qti-prompt")
            question_prompt.text = question.text
            for an in question.answers:
                question_answer = ET.SubElement(
                    question_inter, "qti-simple-choice")
                question_answer.set("identifier", str(an.id))
                question_answer.set("fixed", "false")
                question_answer.text = an.text

            question_proccesing = ET.SubElement(
                question_xml, "qti-response-processing")
            question_proccesing.set("template", "")

            tree1._setroot(question_xml)
            tree1.write(bio1, encoding='UTF-8', xml_declaration=True)

            myzip.writestr("questions/test" +
                           str(test.id) + "-" + str(question.id) + ".xml", bio1.getvalue())

        tree._setroot(root)

        tree.write(bio, encoding='UTF-8', xml_declaration=True)

        myzip.writestr("test" + str(test.id) + ".xml", bio.getvalue())

    data.seek(0)

    return send_file(data, attachment_filename=test_name + '.zip', mimetype='application/zip', as_attachment=True)


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
        p = Problem.query.filter_by(id=question['problem']).first()
        q = Question(text=question['text'])
        p.questions.append(q)
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
    def __init__(self, id, author, test_name, disabled):
        self.id = id
        self.author = author
        self.test_name = test_name
        self.disabled=disabled

    def serialize(self):
        return {
            'id': self.id,
            'author': self.author,
            'test_name': self.test_name,
            'disabled': self.disabled,

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
        if not tookTest(test, current_user):
            tests_list.append(TestDTO(test.id, user.username, test.name, False))
        else:
            tests_list.append(TestDTO(test.id, user.username, test.name, True))


    return jsonify({'tests': [test.serialize() for test in tests_list]}), 200

def tookTest(new_test, user):

    student_answers = user.answers

    questions = []

    for sa in student_answers:
         a = Answer.query.filter_by(id=sa.answer_id).first()
         if a.question_id not in questions:
            questions.append(a.question_id)

    tests=[]
    for q in questions:
        question = TestQuestions.query.filter_by(question_id=q).first()
        test = Test.query.filter_by(id=question.test_id).first()
        if test not in tests:
            tests.append(test)

    if new_test in tests:
        return True
    else:
        return False



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
        return jsonify({'message': "student dont exist"}), 400

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

