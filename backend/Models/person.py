from flaskblog import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"