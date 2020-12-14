from flask import request, Blueprint
from flaskapp.auth import token_required
from flaskapp.services import user_service

user = Blueprint('user', __name__)


@user.route('/users', methods=['GET'])
@token_required
def getAllUsers(current_user):
    return user_service.getUsers()

@user.route('/subject-to-users', methods=['POST'])
@token_required
def addSubjectsToUser(current_user):
    data = request.get_json()

    return user_service.addSubjectsToUser(data)
