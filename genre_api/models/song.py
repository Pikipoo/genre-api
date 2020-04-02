from peewee import *
from flask_restful_swagger import swagger
from flask_restful import fields as flask_fields
from marshmallow import Schema, fields
from genre_api.models.meta import BaseModel
from genre_api.models.singer import Singer
from genre_api.models.genre import Genre


@swagger.model
class Song(BaseModel):
    resource_fields = {
        'id': flask_fields.Integer(),
        'title': flask_fields.String(),
        'singer_id': flask_fields.Integer(),
        'genre_id': flask_fields.Integer()

    }

    id = AutoField()
    title = CharField(index=True)
    singer_id = ForeignKeyField(Singer, backref='songs')
    genre_id = ForeignKeyField(Genre, backref='songs')


@swagger.model
class SongSchema(Schema):
    resource_fields = {
        'title': flask_fields.String(),
        'singer_id': flask_fields.Integer(),
        'genre_id': flask_fields.Integer()

    }

    title = fields.String(required=True)
    singer_id = fields.Integer(required=True)
    genre_id = fields.Integer(required=True)
