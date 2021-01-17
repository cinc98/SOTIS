from flask import request, Blueprint, jsonify
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


@user.route('/student-tests', methods=['GET'])
@token_required
def getStudentTests(current_user):

    return user_service.getStudentTests(current_user)


@user.route('/student-answers/<string:test_name>', methods=['GET'])
@token_required
def getStudentAnswers(current_user, test_name):

    return user_service.getStudentAnswers(current_user, test_name)
