from peewee import *
from flask_restful_swagger import swagger
from flask_restful import fields as flask_fields
from marshmallow import Schema, fields
from genre_api.models.meta import BaseModel
from genre_api.models.genre import Genre


@swagger.model
class Playlist(BaseModel):
    resource_fields = {
        'id': flask_fields.Integer(),
        'name': flask_fields.String(),
        'genre_id': flask_fields.Integer(),
    }

    id = AutoField()
    name = CharField(index=True)
    genre_id = ForeignKeyField(Genre, backref='playlists', null=True)


class PlaylistSchema(Schema):
    name = fields.String(required=True)


class AddSongsSchema(Schema):
    song_ids = fields.List(fields.Integer(), required=True)


@swagger.model
class AddSongsParam():
    resource_fields = {
        'song_ids': flask_fields.List(flask_fields.Integer())
    }
