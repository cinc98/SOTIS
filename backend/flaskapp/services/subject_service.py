from flaskapp.models import Subject, Domain
from flaskapp import db
from flask import jsonify


def add_subject(subject):

    subject_code = subject.get('subject_code')
    subject_name = subject.get('subject_name')

    subject = Subject.query.filter_by(name=subject_name).first()
    if subject:
        return jsonify({'message': "this subject name is taken"}), 400


    subject = Subject.query.filter_by(code=subject_code).first()
    if subject:
        return jsonify({'message': "this subject code is taken"}), 400

    new_subject = Subject(name=subject_name, code=subject_code)

    db.session.add(new_subject)
    db.session.commit()

    return jsonify({'message': "successfully added subject"}), 200


def add_domain(domain):

    domain_title = domain.get('domain_title')
    domain_description = domain.get('domain_description')
    subject_id = domain.get('subject_id')

    subject = Subject.query.filter_by(name=subject_id).first()
    if not subject:
        return jsonify({'message': "this subject dont exist"}), 400

    domain = Domain.query.filter_by(title=domain_title).first()
    if domain:
        return jsonify({'message': "this domain title is taken"}), 400

    subject.domain = Domain(title=domain_title, description=domain_description)
    db.session.add(subject)
    db.session.commit()

    return jsonify({'message': "successfully added domain"}), 200


def get_subjects():
    return jsonify({'subjects': [s.serialize() for s in Subject.query.all()]}), 200


