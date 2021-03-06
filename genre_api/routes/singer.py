from flask import request
from flask_restful import Resource, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import DoesNotExist
from marshmallow import ValidationError
from genre_api.models.singer import *
from genre_api.models.genre import Genre
from genre_api.models.song import Song
from genre_api.models.playlist import Playlist
from genre_api.models.song_to_playlist import SongToPlaylist


class SingerRoute(Resource):
    @swagger.operation(
        notes='get all singer items',
        responseClass=Singer.__name__,
        nickname='get'
    )
    @marshal_with(Singer.resource_fields)
    def get(self):
        query = Singer.select().dicts()

        return [row for row in query]

    @swagger.operation(
        notes='post a singer item',
        responseClass=Singer.__name__,
        nickname='post',
        parameters=[
            {
                'name': 'body',
                'description': 'The added singer',
                'required': True,
                'allowMultiple': False,
                'dataType': SingerSchema.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 400,
                'message': 'Invalid JSON schema'
            },
            {
                'code': 404,
                'message': 'Genre with ID <genre_id> not found'
            }
        ]
    )
    @marshal_with(Singer.resource_fields)
    def post(self):
        json_data = request.get_json()
        try:
            SingerSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        genre_id = json_data['genre_id']
        try:
            genre = Genre.get(Genre.id == genre_id)
        except DoesNotExist:
            abort(404, message=f'Genre with ID {genre_id} not found')

        singer_name = json_data['name']
        singer = Singer.create(name=singer_name, genre_id=genre.id,
                               inferred_genre_id=None)

        return singer.select().where(Singer.id == singer.id).dicts().get()


class SingerByIDRoute(Resource):
    @swagger.operation(
        notes='get a singer item by ID',
        responseClass=Singer.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'singer_id',
                'description': 'The ID of the retrieved singer',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Singer with ID <singer_id> not found'
            }
        ]
    )
    @marshal_with(Singer.resource_fields)
    def get(self, singer_id):
        try:
            query = Singer.select().where(Singer.id == singer_id).dicts().get()
        except DoesNotExist:
            abort(404, message=f'Singer with ID {singer_id} not found')

        return query

    @swagger.operation(
        notes='update a singer item by ID',
        responseClass=Singer.__name__,
        nickname='put',
        parameters=[
            {
                'name': 'singer_id',
                'description': 'The ID of the updated singer',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            },
            {
                'name': 'body',
                'description': 'The updated singer values',
                'required': True,
                'allowMultiple': False,
                'dataType': SingerPutSchema.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Singer with ID <singer_id> not found'
            }
        ]
    )
    @marshal_with(Singer.resource_fields)
    def put(self, singer_id):
        json_data = request.get_json()
        try:
            SingerPutSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        # Getting singer item
        try:
            singer = Singer.get(Singer.id == singer_id)
        except DoesNotExist:
            abort(404, message=f'Singer with ID {singer_id} not found')

        # Verifying genre exists
        genre_id = json_data['genre_id']
        try:
            genre = Genre.get(Genre.id == genre_id)
        except DoesNotExist:
            abort(404, message=f'Genre with ID {genre_id} not found')
        singer.genre_id = genre_id

        singer_name = json_data['name']
        singer.name = singer_name
        inferred_genre_id = json_data['inferred_genre_id']
        singer.inferred_genre_id = inferred_genre_id

        with singer._meta.database.atomic():
            singer.save()

        return singer.select().where(Singer.id == singer_id).dicts().get()


class SingerSongsRoute(Resource):
    @swagger.operation(
        notes='get a singer item by ID',
        responseClass=Song.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'singer_id',
                'description': 'The ID of the retrieved singer',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Singer with ID <singer_id> not found'
            }
        ]
    )
    @marshal_with(Song.resource_fields)
    def get(self, singer_id):
        try:
            singer = Singer.get(Singer.id == singer_id)
        except DoesNotExist:
            abort(404, message=f'Singer with ID {singer_id} not found')

        return [song for song in singer.songs.select().dicts()]


class SingerPlaylistsRoute(Resource):
    @swagger.operation(
        notes='get playlists item by singer ID',
        responseClass=Playlist.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'singer_id',
                'description': 'The ID of the singer',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Singer with ID <singer_id> not found'
            }
        ]
    )
    @marshal_with(Playlist.resource_fields)
    def get(self, singer_id):
        try:
            songs = Song.get(Song.singer_id == singer_id).alias('songs')
            singer_playlists = Playlist.select()\
                                       .distinct()\
                                       .join(SongToPlaylist)\
                                       .join(songs)\
                                       .where(
                                           SongToPlaylist.song_id == songs.id
                                           )\
                                       .where(songs.singer_id == singer_id)
        except DoesNotExist:
            abort(404, message=f'Singer with ID {singer_id} not found')

        return [playlist for playlist in singer_playlists.select().dicts()]
