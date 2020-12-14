from flask import request, Blueprint
from flaskapp.auth import token_required
from flaskapp.services import subject_service

subject = Blueprint('subject', __name__)


@subject.route('/add-subject', methods=['POST'])
@token_required
def signup_post(current_user):
    data = request.get_json()

    return subject_service.addSubject(data)


@subject.route('/subjects', methods=['GET'])
@token_required
def getAllSubjects(current_user):
    return subject_service.getSubjects()

