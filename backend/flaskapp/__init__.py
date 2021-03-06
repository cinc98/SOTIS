from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:user@localhost/flask-sotisdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .routes import routes as routes_blueprint
app.register_blueprint(routes_blueprint)

from .routess.subject_routes import subject as subject_blueprint
app.register_blueprint(subject_blueprint)

from .routess.user_routes import user as user_blueprint
app.register_blueprint(user_blueprint)

from .routess.ks_routes import ks as ks_blueprint
app.register_blueprint(ks_blueprint)

from flaskapp import routes
