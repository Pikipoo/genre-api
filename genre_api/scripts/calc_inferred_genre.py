import requests
import json
import operator
import logging
from genre_api.config.config import CONFIG
from collections import defaultdict
from genre_api.scripts.errors import APIError

URL = f"http://{CONFIG['flask']['host']}:5000"


def get_all_singers():
    """
    Retrieve all singers from API.
    """
    rq = requests.get(f'{URL}/singers')
    return rq.status_code, rq.json()


def get_playlists_for_singer(singer):
    """
    Retrieve all playlist a singer is in from API.
    """
    rq = requests.get(f"{URL}/singers/{singer['id']}/playlists")
    return rq.status_code, rq.json()


def count_playlist_genre(playlists_array):
    """
    Creates a directory referencing every music genre by id and counting their
    occurrences in playlists_array.
    """
    genre_count_dict = defaultdict(int)
    for playlist in playlists_array:
        playlist_genre = playlist['genre_id']
        genre_count_dict[playlist_genre] += 1

    return genre_count_dict


def update_singer_genre(singer, inferred_genre_id):
    """
    Use the API to update a singer's inferred_genre using calc_inferred_genre
    calculations.
    """
    singer_update = {
        'name': singer['name'],
        'genre_id': singer['genre_id'],
        'inferred_genre_id': inferred_genre_id
    }
    rq = requests.put(f"{URL}/singers/{singer['id']}", json=singer_update)
    return rq.status_code, rq.json()


def calc_inferred_genre():
    """
    Retrieve playlists for every singers and update singers' inferred_genre
    based on the playlists' genre they appear most in.
    """
    rsp_code, singers_array = get_all_singers()
    if rsp_code != 200:
        raise APIError(rsp_code, singers_array)

    for singer in singers_array:
        rsp_code, playlists_array = get_playlists_for_singer(singer)
        if rsp_code != 200:
            logging.warning(f'{rsp_code} - {singers_array}')
            continue
        genre_count_dict = count_playlist_genre(playlists_array)
        # Get the key with the highest value in genre_count_dict
        inferred_genre_id = max(genre_count_dict.items(),
                                key=operator.itemgetter(1))[0]

        rsp_code, singer = update_singer_genre(singer, inferred_genre_id)
        if rsp_code != 200:
            logging.warning(f'{rsp_code} - {singers_array}')
            continue


if __name__ == '__main__':
    calc_inferred_genre()
