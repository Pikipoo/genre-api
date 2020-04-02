from flask import request
from flask_restful import Resource, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import DoesNotExist, chunked
from marshmallow import ValidationError
from genre_api.models.playlist import *
from genre_api.models.genre import Genre
from genre_api.models.song import Song
from genre_api.models.song_to_playlist import SongToPlaylist
from genre_api.models.singer import Singer
from genre_api.routes.song import SongByIDRoute


class PlaylistRoute(Resource):
    @swagger.operation(
        notes='get all playlist items',
        responseClass=Playlist.__name__,
        nickname='get'
    )
    @marshal_with(Playlist.resource_fields)
    def get(self):
        query = Playlist.select().dicts()

        return [row for row in query]

    @swagger.operation(
        notes='post a playlist item',
        responseClass=Playlist.__name__,
        nickname='post',
        parameters=[
            {
                'name': 'body',
                'description': 'The added playlist',
                'required': True,
                'allowMultiple': False,
                'dataType': Playlist.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 400,
                'message': 'Invalid JSON schema'
            }
        ]
    )
    @marshal_with(Playlist.resource_fields)
    def post(self):
        json_data = request.get_json()
        try:
            PlaylistSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        playlist_name = json_data['name']
        playlist = Playlist.create(name=playlist_name, genre_id=None)

        return playlist.select().where(Playlist.id == playlist.id)\
            .dicts().get()


class PlaylistByIDRoute(Resource):
    @swagger.operation(
        notes='get a playlist item by ID',
        responseClass=Playlist.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'playlist_id',
                'description': 'The ID of the retrieved playlist',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Playlist with ID <playlist_id> not found'
            }
        ]
    )
    @marshal_with(Playlist.resource_fields)
    def get(self, playlist_id):
        try:
            query = Playlist.select().where(Playlist.id == playlist_id)\
                .dicts().get()
        except DoesNotExist:
            abort(404, message=f'Playlist with ID {playlist_id} not found')

        return query


class PlaylistAddSongsRoute(Resource):
    @swagger.operation(
        notes='post list of song items in a playlist',
        responseClass=Song.__name__,
        nickname='post',
        parameters=[
            {
                'name': 'playlist_id',
                'description': 'The ID of the playlist',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            },
            {
                'name': 'body',
                'description': 'The added songs',
                'required': True,
                'allowMultiple': False,
                'dataType': AddSongsParam.__name__,
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
                'message': 'Playlist with ID <playlist_id> not found'
            },
            {
                'code': 404,
                'message': 'Song with ID <song_id> not found'
            }
        ]
    )
    @marshal_with(Song.resource_fields)
    def post(self, playlist_id):
        json_data = request.get_json()
        try:
            AddSongsSchema().load(json_data)
        except ValidationError as error:
            abort(400, message=error.messages)

        songs_array = self.__verify_songs_from_id(json_data['song_ids'])
        songs_to_playlist = [SongToPlaylist(
            song_id=song['id'], playlist_id=playlist_id
            ) for song in songs_array]

        # Start transaction.
        # SongToPlaylist._meta referes to the Meta subclass of BaseModel.
        with SongToPlaylist._meta.database.atomic():
            try:
                SongToPlaylist.bulk_create(songs_to_playlist, batch_size=100)
            except DoesNotExist:
                abort(404, message=f'Playlist with ID {playlist_id} not found')

        return [song for song in songs_array]

    def __verify_songs_from_id(self, song_ids_list):
        """
        Get all songs in the database from a list of ids.
        It ensures that the povided song ids are found in the database while
        allowing to return the added songs.
        """
        songs_array = []
        for given_song_id in song_ids_list:
            song_id = SongByIDRoute().get(given_song_id)
            songs_array.append(song_id)

        return songs_array

    @swagger.operation(
        notes='get songs in a playlist',
        responseClass=Song.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'playlist_id',
                'description': 'The ID of the playlist',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Playlist with ID <playlist_id> not found'
            }
        ]
    )
    @marshal_with(Song.resource_fields)
    def get(self, playlist_id):
        try:
            songs_in_playlist = Song.select()\
                                    .join(SongToPlaylist)\
                                    .join(Playlist)\
                                    .where(Playlist.id == playlist_id)
        except DoesNotExist:
            abort(404, message=f'Playlist with ID {singer_id} not found')

        return [song for song in songs_in_playlist.select().dicts()]


class PlaylistSingerRoute(Resource):
    @swagger.operation(
        notes='get singers in a playlist',
        responseClass=Singer.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'playlist_id',
                'description': 'The ID of the playlist',
                'required': True,
                'allowMultiple': False,
                'dataType': int.__name__,
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 404,
                'message': 'Playlist with ID <playlist_id> not found'
            }
        ]
    )
    @marshal_with(Singer.resource_fields)
    def get(self, playlist_id):
        try:
            singers_in_playlist = Singer.select()\
                                        .distinct()\
                                        .join(
                                            Song,
                                            on=(Singer.id == Song.singer_id)
                                            )\
                                        .switch(Song)\
                                        .join(SongToPlaylist)\
                                        .join(Playlist)\
                                        .where(Playlist.id == playlist_id)
        except DoesNotExist:
            abort(404, message=f'Playlist with ID {singer_id} not found')

        return [singer for singer in singers_in_playlist.select().dicts()]
