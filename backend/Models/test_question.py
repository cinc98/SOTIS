from flaskblog import db

class Test_question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    