from flask import request
from flask_restful import Resource, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import DoesNotExist
from marshmallow import ValidationError
from genre_api.models.song import Song, SongSchema
from genre_api.models.singer import Singer
from genre_api.models.genre import Genre
from genre_api.models.playlist import Playlist
from genre_api.models.song_to_playlist import SongToPlaylist


class SongRoute(Resource):
    @swagger.operation(
        notes='get all song items',
        responseClass=Song.__name__,
        nickname='get'
    )
    @marshal_with(Song.resource_fields)
    def get(self):
        query = Song.select().dicts()

        return [row for row in query]

    @swagger.operation(
        notes='post a song item',
        responseClass=Song.__name__,
        nickname='post',
        parameters=[
            {
                'name': 'body',
                'description': 'The added song',
                'required': True,
                'allowMultiple': False,
                'dataType': SongSchema.__name__,
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
                'message': 'Singer with ID <singer_id> not found'
            },
            {
                'code': 404,
                'message': 'Genre with ID <genre_id> not found'
            }
        ]
    )
    @marshal_with(Song.resource_fields)
    def post(self):
        json_data = request.get_json()
        try:
            SongSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        singer_id = json_data['singer_id']
        try:
            singer = Singer.get(Singer.id == singer_id)
        except DoesNotExist:
            abort(404, message=f'Singer with ID {singer_id} not found')

        genre_id = json_data['genre_id']
        try:
            genre = Genre.get(Genre.id == genre_id)
        except DoesNotExist:
            abort(404, message=f'Genre with ID {genre_id} not found')

        song_title = json_data['title']
        song = Song.create(title=song_title, singer_id=singer.id,
                           genre_id=genre.id)

        return song.select().where(Song.id == song.id).dicts().get()


class SongByIDRoute(Resource):
    @swagger.operation(
        notes='get a song item by ID',
        responseClass=Song.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'song_id',
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
                'message': 'Song with ID <song_id> not found'
            }
        ]
    )
    @marshal_with(Song.resource_fields)
    def get(self, song_id):
        try:
            query = Song.select().where(Song.id == song_id).dicts().get()
        except DoesNotExist:
            abort(404, message=f'Song with ID {song_id} not found')

        return query


class SongPlaylistsRoute(Resource):
    @swagger.operation(
        notes='get playlist items for a song',
        responseClass=Playlist.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'song_id',
                'description': 'The ID of the song',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Song with ID <song_id> not found'
            }
        ]
    )
    @marshal_with(Playlist.resource_fields)
    def get(self, song_id):
        try:
            playlists_have_song = Playlist.select()\
                                          .distinct()\
                                          .join(SongToPlaylist)\
                                          .join(Song)\
                                          .where(Song.id == song_id)
        except DoesNotExist:
            abort(404, message=f'Song with ID {song_id} not found')

        return [playlist for playlist in playlists_have_song.select().dicts()]
