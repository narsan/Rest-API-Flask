import datetime
from db import db


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    approved = db.Column(db.BOOLEAN)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))

    def __init__(self, comment, movie_id):
        self.comment = comment
        self.approved = False
        self.created_at = datetime.datetime.now()
        self.movie_id = movie_id

    def json(self):
        return {'comment': self.comment, 'approved': self.approved}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
