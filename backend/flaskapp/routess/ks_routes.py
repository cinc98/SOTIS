from flask import request, Blueprint
from flaskapp.auth import token_required
from flaskapp.services import ks_service

ks = Blueprint('ks', __name__)


@ks.route('/add-ks', methods=['POST'])
@token_required
def add_ks(current_user):
    data = request.get_json()

    return ks_service.add_ks(data)


@ks.route('/kss/<string:domain_title>', methods=['GET'])
@token_required
def get_ks_by_domain(current_user, domain_title):

    return ks_service.get_ks_by_domain(domain_title)


@ks.route('/ks/<string:ks_title>', methods=['GET'])
@token_required
def get_ks_by_title(current_user, ks_title):
    
    return ks_service.get_ks_by_title(ks_title)

@ks.route('/ks-id/<string:ks_id>', methods=['GET'])
@token_required
def get_ks_by_id(current_user, ks_id):
    
    return ks_service.get_ks_by_id(ks_id)

@ks.route('/ks-subject/<string:subject_title>', methods=['GET'])
@token_required
def get_ks_by_subject(current_user, subject_title):
    
    return ks_service.get_ks_by_subject(subject_title)
