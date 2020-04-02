from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, marshal_with
from flask_restful_swagger import swagger
from peewee import *


def create_routes(api):
    pass


def create_app():
    app = Flask(__name__)
    return app


def create_api(app):
    api = swagger.docs(Api(app), apiVersion='0.1')
    return api


def create_tables():
    with database:
        database.create_tables([Genre, Singer, Song, Playlist, SongToPlaylist])
