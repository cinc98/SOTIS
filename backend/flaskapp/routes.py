from flaskapp.models import User, UserAnswers, UserRoles, UserSubjects, UserTests, Role, Answer, Question, QuestionAnswers, Test, TestQuestions, Subject
from flask import Blueprint

routes = Blueprint('routes', __name__)