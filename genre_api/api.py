from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import *
from genre_api.models.meta import sqlite_db as database
from genre_api.models.genre import Genre
from genre_api.models.singer import Singer
from genre_api.models.song import Song
from genre_api.models.playlist import Playlist
from genre_api.models.song_to_playlist import SongToPlaylist
from genre_api.routes.genre import *
from genre_api.routes.singer import *
from genre_api.routes.song import *
from genre_api.routes.playlist import *


def create_routes(api):
    api.add_resource(SingerRoute, '/singers')
    api.add_resource(SingerByIDRoute, '/singers/<singer_id>')
    api.add_resource(SingerSongsRoute, '/singers/<singer_id>/songs')
    api.add_resource(SingerPlaylistsRoute, '/singers/<singer_id>/playlists')

    api.add_resource(GenreRoute, '/genres')
    api.add_resource(GenreByIDRoute, '/genres/<genre_id>')

    api.add_resource(SongRoute, '/songs')
    api.add_resource(SongByIDRoute, '/songs/<song_id>')
    api.add_resource(SongPlaylistsRoute, '/songs/<song_id>/playlists')

    api.add_resource(PlaylistRoute, '/playlists')
    api.add_resource(PlaylistByIDRoute, '/playlists/<playlist_id>')
    api.add_resource(PlaylistAddSongsRoute, '/playlists/<playlist_id>/songs')
    api.add_resource(PlaylistSingerRoute, '/playlists/<playlist_id>/singers')


def create_app():
    app = Flask(__name__)
    return app


def create_api(app):
    api = swagger.docs(Api(app), apiVersion='0.1')
    return api


def create_tables():
    with database:
        database.create_tables([Genre, Singer, Song, Playlist, SongToPlaylist])
