from flask import request
from flask_restful import Resource, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import IntegrityError
from marshmallow import ValidationError
from genre_api.models.genre import Genre, GenreSchema


class GenreRoute(Resource):
    @swagger.operation(
        notes='get all genre items',
        responseClass=Genre.__name__,
        nickname='get'
    )
    @marshal_with(Genre.resource_fields)
    def get(self):
        query = Genre.select().dicts()

        return [row for row in query]

    @swagger.operation(
        notes='post a genre item',
        responseClass=Genre.__name__,
        nickname='post',
        parameters=[
            {
                'name': 'body',
                'description': 'The added genre',
                'required': True,
                'allowMultiple': False,
                'dataType': Genre.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 400,
                'message': 'Invalid JSON schema'
            },
            {
                'code': 409,
                'message': 'Genre {genre_name} already exists'
            }
        ]
    )
    @marshal_with(Genre.resource_fields)
    def post(self):
        json_data = request.get_json()
        try:
            GenreSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        genre_name = json_data['name']
        try:
            genre = Genre.create(name=genre_name)
        except IntegrityError:
            abort(409, message=f'Genre {genre_name} already exists')

        return genre.select().where(Genre.id == genre.id).dicts().get()
