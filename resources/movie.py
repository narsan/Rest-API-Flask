from flask_restful import Resource, reqparse
from models.movie import MovieModel
from flask import request
from authentication import check_authority
import jwt


class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Movie need a name"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        movie = MovieModel.find_by_id(id)
        if movie:
            return movie.json()
        return {'message': 'Movie not found'}, 404

    @check_authority
    def post(self):
        data = request.get_json()
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 1:
            name = data['name']
            description = data['description']
            movie = MovieModel(name, description)

            try:
                movie.save_to_db()
            except:
                return {'message': "An error occurred inserting the movie."}, 500

            return movie.json(), 201
        else:
            return {'message': 'Only admin can insert a movie'}

    @check_authority
    def delete(self, id):
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 1:

            movie = MovieModel.find_by_id(id)
            if movie:
                movie.delete_from_db()
                return {'message': 'Movie deleted'}
            else:
                return {'message': 'Movie not found'}, 404
        else:
            return {'message': 'Only admin can delete a movie'}

    @check_authority
    def put(self, id):
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        if token['role'] == 1:
            data = request.get_json()

            movie = MovieModel.find_by_id(id)

            if movie:
                try:
                    movie.name = data['name']
                    movie.description = data['description']
                    movie.save_to_db()
                    return movie.json()
                except:
                    return {"message": "An error occurred updating the movie."}, 500
            else:
                return {'message': 'movie not found to update.'}, 404
        else:
            return {'message': 'Only admin can update a movie'}


class MovieList(Resource):
    def get(self):
        return {'movies': list(map(lambda x: x.json(), MovieModel.query.all()))}
