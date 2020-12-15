from flask import request, Blueprint
from flaskapp.auth import token_required
from flaskapp.services import subject_service

subject = Blueprint('subject', __name__)


@subject.route('/add-subject', methods=['POST'])
@token_required
def add_subject(current_user):
    data = request.get_json()

    return subject_service.add_subject(data)


@subject.route('/add-domain', methods=['POST'])
@token_required
def add_domain(current_user):
    data = request.get_json()

    return subject_service.add_domain(data)

@subject.route('/subjects', methods=['GET'])
@token_required
def get_all_subjects(current_user):
    return subject_service.get_subjects()



