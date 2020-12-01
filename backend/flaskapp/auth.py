from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flaskapp.models import User
from flaskapp import db, app, bcrypt
import jwt
import datetime
from functools import wraps


auth = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except: 
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.get_json()

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user: 
        return jsonify({'message': "this username is taken"}), 400

    new_user = User(email=email, username=username, password=bcrypt.generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': "successful registration"}), 200

@auth.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': "wrong username or password"}), 400

    token = jwt.encode({'username' : user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)}, app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')}), 200

@auth.route('/user', methods=['GET'])
@token_required
def get_logged_user(current_user):
    return jsonify({'user': current_user.serialize()}), 200 




