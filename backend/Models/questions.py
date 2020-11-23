from flaskblog import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    