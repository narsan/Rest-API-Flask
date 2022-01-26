from db import db


class MovieModel(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(500))
    votes = db.relationship('VoteModel', lazy='dynamic')
    comments = db.relationship('CommentModel', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def average(self, lst):
        if len(lst) != 0:
            return float(sum(d['vote'] for d in lst)) / len(lst)
        return 0

    def json(self):
        return {'name': self.name, 'description': self.description,
                'votes': self.average([vote.json() for vote in self.votes.all()]),
                'comments': [comment.json() for comment in self.comments.all()]}

    @classmethod
    def find_by_id(cls, movie_id):
        return cls.query.filter_by(movie_id=movie_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
