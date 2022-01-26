from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, role, username, password):
        self.role = role
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'role': self.role, 'username': self.username, 'password': self.password}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
