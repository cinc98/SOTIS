from flaskblog import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   