import unittest
import pytest
import json
from peewee import SqliteDatabase
from genre_api.models.genre import Genre
from genre_api.models.singer import Singer
from genre_api.models.song import Song
from genre_api.models.playlist import Playlist
from genre_api.models.song_to_playlist import SongToPlaylist

MODELS = [Genre, Singer, Song, Playlist, SongToPlaylist]


@pytest.mark.usefixtures('app_class')
class TestGenre(unittest.TestCase):
    database = SqliteDatabase(':memory:')

    def setUp(self):
        self.database.bind(MODELS, bind_refs=False, bind_backrefs=False)
        self.database.connect()
        self.database.create_tables(MODELS)

    def tearDown(self):
        self.database.drop_tables(MODELS)
        self.database.close()

    def test_post_genre_200(self):
        body = json.dumps({
            'name': 'Genre1'
            })
        response = self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)

        self.assertEqual(response.status_code, 200)

    def test_post_genre_400(self):
        body = json.dumps({})
        response = self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)

        self.assertEqual(response.status_code, 400)

    def test_post_genre_200(self):
        body = json.dumps({
            'name': 'Genre1'
            })

        self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)
        response = self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)

        self.assertEqual(response.status_code, 409)

    def test_get_genre(self):
        body = json.dumps({
            'name': 'Genre1'
            })
        self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)

        response_body = [{
            'id': 1,
            'name': 'Genre1'}]
        response = self.client.get('/genres')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, response_body)
