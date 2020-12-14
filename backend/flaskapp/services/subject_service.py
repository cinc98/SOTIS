from flaskapp.models import Subject
from flaskapp import db
from flask import jsonify


def addSubject(subject):

    subject_code = subject.get('subject_code')
    subject_name = subject.get('subject_name')

    subject = Subject.query.filter_by(name=subject_name).first()

    if subject:
        return jsonify({'message': "this subject name is taken"}), 400

    new_subject = Subject(name=subject_name, code=subject_code)

    db.session.add(new_subject)
    db.session.commit()

    return jsonify({'message': "successfully added subject"}), 200