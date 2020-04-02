import requests
import json
from errors import APIError

URL = 'http://localhost:5000'


def get_all_singers():
    rq = requests.get(f'{URL}/singers')
    return rq.status_code, rq.json()


def get_playlists_for_singer(singer):
    rq = requests.get(f"{URL}/singers/{singer['id']}/playlists")
    return rq.status_code, rq.json()


def calc_inferred_genre():
    rsp_code, singers_array = get_all_singers()
    if rsp_code != 200:
        raise APIError(rsp_code, singers_array)

    for singer in singers_array:
        rsp_code, singer_playlists_array = get_playlists_for_singer(singer)
        if rsp_code != 200:
            continue
        print(singer_playlists_array)


if __name__ == '__main__':
    calc_inferred_genre()
