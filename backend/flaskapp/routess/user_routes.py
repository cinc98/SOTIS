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


@user.route('/student-tests/<string:username>', methods=['GET'])
def getStudentTests(username):

    return user_service.getStudentTests(username)


@user.route('/student-answers/<string:username>/<string:test_name>', methods=['GET'])
def getStudentAnswers(username, test_name):

    return user_service.getStudentAnswers(username, test_name)

@user.route('/students', methods=['GET'])
@token_required
def getStudents(current_user):
    return user_service.getStudents(current_user)
