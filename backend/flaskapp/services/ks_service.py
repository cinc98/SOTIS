from flaskapp.models import KnowledgeSpace, Domain, Problem, Link
from flaskapp import db
from flask import jsonify


def add_ks(data):

    ks_title = data.get('ks_title')
    domain_title = data.get('domain_title')
    problems = data.get('nodes')
    links = data.get('links')

    domain = Domain.query.filter_by(title=domain_title).first()

    if not domain:
        return jsonify({'message': "this domain dont exist"}), 400

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



