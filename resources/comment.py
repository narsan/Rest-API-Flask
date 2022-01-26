from flask_restful import Resource, reqparse
from models.comment import CommentModel
from flask import Flask, request
from authentication import check_authority
import jwt


class Comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('comment_body',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('approved',
                        type=bool,
                        required=True,
                        help="We need to know if the comment approved"
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
            comment = CommentModel(data['comment_body'], data['movie_id'])

            try:
                comment.save_to_db()
            except:
                return {"message": "An error occurred inserting the comment."}, 500

            return comment.json(), 201
        else:
            return {'message': 'Only users can add comments'}

    @check_authority
    def delete(self, id):
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 1:
            comment = CommentModel.find_by_id(id)
            if comment:
                comment.delete_from_db()
                return {'message': 'Comment deleted.'}, 204
            return {'message': 'Comment not found.'}, 404
        else:
            return {'message': 'Only admin can delete comments'}

    @check_authority
    def put(self, id):
        data = request.get_json()
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 1:
            comment = CommentModel.find_by_id(id)
            if comment:
                try:
                    comment.approved = data['approved']
                    comment.save_to_db()
                    return comment.json(), 204

                except:
                    return {"message": "An error occurred updating the item."}, 500
            return {'message': 'comment not found to update.'}, 404
        else:
            return {'message': 'Only admin can update comments'}


class CommentList(Resource):
    def get(self):
        return {'comments': list(map(lambda x: x.json(), CommentModel.query.all()))}
