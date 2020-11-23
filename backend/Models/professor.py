from flaskblog import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    