from flaskapp.models import User, Subject
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
