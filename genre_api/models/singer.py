from peewee import *
from flask_restful_swagger import swagger
from flask_restful import fields as flask_fields
from marshmallow import Schema, fields
from genre_api.models.meta import BaseModel
from genre_api.models.genre import Genre


@swagger.model
class Singer(BaseModel):
    resource_fields = {
        'id': flask_fields.Integer(),
        'name': flask_fields.String(),
        'genre_id': flask_fields.Integer(),
        'inferred_genre_id': flask_fields.Integer()
    }

    id = AutoField()
    name = CharField(index=True)
    genre_id = ForeignKeyField(Genre, backref='singers')
    inferred_genre_id = ForeignKeyField(Genre, backref='inferred_singers',
                                        null=True)


class SingerSchema(Schema):
    name = fields.String(required=True)
    genre_id = fields.Integer(required=True)
