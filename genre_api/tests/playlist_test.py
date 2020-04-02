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
class TestPlaylist(unittest.TestCase):
    database = SqliteDatabase(':memory:')

    def setUp(self):
        self.database.bind(MODELS, bind_refs=False, bind_backrefs=False)
        self.database.connect()
        self.database.create_tables(MODELS)

    def tearDown(self):
        self.database.drop_tables(MODELS)
        self.database.close()

    def test_post_playlist_200(self):
        body = json.dumps({
            'name': 'Playlist1'
            })
        response = self.client.post(
            '/playlists',
            headers={'Content-Type': 'application/json'},
            data=body)

        self.assertEqual(response.status_code, 200)

    def test_get_playlist(self):
        body = json.dumps({
            'name': 'Playlist1'
            })
        self.client.post(
            '/playlists',
            headers={'Content-Type': 'application/json'},
            data=body)

        response_body = [{
            'id': 1,
            'name': 'Playlist1',
            'genre_id': 0
            }]
        response = self.client.get('/playlists')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, response_body)

    def test_get_playlist_by_id_200(self):
        body = json.dumps({
            'name': 'Playlist1'
            })
        self.client.post(
            '/playlists',
            headers={'Content-Type': 'application/json'},
            data=body)

        response_body = {
            'id': 1,
            'name': 'Playlist1',
            'genre_id': 0
            }
        response = self.client.get('/playlists/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, response_body)

    def test_post_song_to_playlist_200(self):
        body = json.dumps({
            'name': 'Genre1'
            })
        self.client.post(
            '/genres',
            headers={'Content-Type': 'application/json'},
            data=body)

        body = json.dumps({
            'name': 'Singer1',
            'genre_id': 1
            })
        self.client.post(
            '/singers',
            headers={'Content-Type': 'application/json'},
            data=body)

        body = [{
            'title': 'Song1',
            'singer_id': 1,
            'genre_id': 1
            },
            {
            'title': 'Song2',
            'singer_id': 1,
            'genre_id': 1
            }]
        for b in body:
            self.client.post(
                '/songs',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(b))

        body = json.dumps({
            'name': 'Playlist1'
            })
        self.client.post(
            '/playlists',
            headers={'Content-Type': 'application/json'},
            data=body)

        body = json.dumps({
            'song_ids': [1, 2]
            })
        response = self.client.post(
            '/playlists/1/songs',
            headers={'Content-Type': 'application/json'},
            data=body)

        self.assertEqual(response.status_code, 200)
