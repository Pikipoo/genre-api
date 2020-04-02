from peewee import *
from flask_restful_swagger import swagger
from flask_restful import fields as flask_fields
from marshmallow import Schema, fields
from genre_api.models.meta import BaseModel


@swagger.model
class Genre(BaseModel):
    resource_fields = {
        'id': flask_fields.Integer(),
        'name': flask_fields.String()
    }

    id = AutoField()
    name = CharField(unique=True, index=True)


class GenreSchema(Schema):
    name = fields.String(required=True)
