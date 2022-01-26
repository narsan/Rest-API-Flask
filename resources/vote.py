from flask_restful import Resource, reqparse
from models.vote import VoteModel
from flask import Flask, request
from authentication import check_authority
import jwt


class Vote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('vote',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('movie_id',
                        type=int,
                        required=True,
                        help="Every vote needs a movie_id."
                        )

    @check_authority
    def post(self):
        data = request.get_json()
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 0:

            vote = VoteModel(data['vote'], data['movie_id'])

            try:
                vote.save_to_db()
            except:
                return {"message": "An error occurred inserting the vote."}, 500

            return vote.json(), 201
        else:
            return {'message': 'Only users can vote'}


class VoteList(Resource):
    def get(self):
        return {'votes': list(map(lambda x: x.json(), VoteModel.query.all()))}
