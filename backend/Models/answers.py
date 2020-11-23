from flaskblog import db

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    