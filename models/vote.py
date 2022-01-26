from db import db


class VoteModel(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))

    def __init__(self, vote, movie_id):
        self.vote = vote
        self.movie_id = movie_id

    def json(self):
        return {'vote': self.vote, 'movieId': self.movie_id}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
