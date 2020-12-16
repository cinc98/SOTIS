from flaskapp.models import KnowledgeSpace, Domain, Problem, Link, Subject
from flaskapp import db
from flask import jsonify

def get_ks_by_domain(domain_title):

    domain = Domain.query.filter_by(title=domain_title).first()

    if not domain:
        return jsonify({'message': "this domain dont exist"}), 400

    knowledge_spaces = domain.knowledge_spaces

    return jsonify({'knowledge_spaces': [ks.serialize() for ks in knowledge_spaces]}), 200

def get_ks_by_title(ks_title):
    
    ks = KnowledgeSpace.query.filter_by(title=ks_title).first()

    if not ks:
        return jsonify({'message': "this knowledge space dont exist"}), 400


    return jsonify({'knowledge_space': ks.serialize()}), 200

def get_ks_by_id(ks_id):
    
    ks = KnowledgeSpace.query.filter_by(id=ks_id).first()

    if not ks:
        return jsonify({'message': "this knowledge space dont exist"}), 400


    return jsonify({'knowledge_space': ks.serialize()}), 200

def get_ks_by_subject(subject_name):
    
    subject = Subject.query.filter_by(name=subject_name).first()

    if not subject:
        return jsonify({'message': "this subject dont exist"}), 400

    domain = subject.domain

    if not domain:
        return jsonify({'message': "this subject dont have domain"}), 400


    knowledge_spaces = domain.knowledge_spaces

    return jsonify({'knowledge_spaces': [ks.serialize() for ks in knowledge_spaces]}), 200


def add_ks(data):

    ks_title = data.get('ks_title')
    domain_title = data.get('domain_title')
    problems = data.get('nodes')
    links = data.get('links')

    domain = Domain.query.filter_by(title=domain_title).first()
    kss = KnowledgeSpace.query.filter_by(title=ks_title).first()

    if not domain:
        return jsonify({'message': "this domain dont exist"}), 400

    if kss:
        return jsonify({'message': "this knowledge space title is taken"}), 400

    ks = KnowledgeSpace(title=ks_title, domain_id=domain.id)


    for p in problems:
        problem = Problem(title=p['node_name'])
        ks.problems.append(problem)
        db.session.add(problem)
    
    db.session.add(ks)
    db.session.commit()

    saved_ks = KnowledgeSpace.query.filter_by(title=ks_title).first()
    for l in links:
        source = Problem.query.filter_by(knowledge_space_id=saved_ks.id).filter_by(title=l['source_name']).first()
        target = Problem.query.filter_by(knowledge_space_id=saved_ks.id).filter_by(title=l['target_name']).first()
        link = Link(source_id=source.id, target_id=target.id)
        saved_ks.links.append(link)
        db.session.add(link)

    db.session.add(ks)
    db.session.commit()

    return jsonify({'message': "successfully created ks"}), 200



