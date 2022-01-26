from flask import Flask
from flask_restful import Api
from db import db
from resources.movie import Movie, MovieList
from resources.comment import Comment, CommentList
from resources.vote import Vote, VoteList
import jwt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'nar'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    if identity == 0:
        return {'is_admin': False, 'user': True, 'guest': False}
    else:
        return {'is_admin': False, 'user': False, 'guest': True}


api.add_resource(Movie, '/movie/<int:id>', '/admin/movie', '/admin/movie/<int:id>')
api.add_resource(MovieList, '/movies')
api.add_resource(Vote, '/user/vote')
api.add_resource(Comment, '/user/comment', '/admin/comment/<int:id>')
api.add_resource(CommentList, '/comments')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
