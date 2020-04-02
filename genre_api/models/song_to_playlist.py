from peewee import *
from flask_restful_swagger import swagger
from flask_restful import fields as flask_fields
from marshmallow import Schema, fields
from genre_api.models.meta import BaseModel
from genre_api.models.genre import Genre
from genre_api.models.song import Song
from genre_api.models.playlist import Playlist


class SongToPlaylist(BaseModel):
    song_id = ForeignKeyField(Song, backref='playlists', index=True)
    playlist_id = ForeignKeyField(Playlist, backref='songs', index=True)
