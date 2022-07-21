from fileinput import filename
import glob
import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('MUSIXMATCH_API_KEY')

"""
TODO:全体的にエラーハンドリングが必要。どんな不足データが返ってくるか考えること。
"""


def get_lyric2(title, file_list_path):
    for file_path in sorted(glob.glob(file_list_path)):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        if title == file_name:
            with open(file_path, newline="") as f:
                data = f.read()
                return data
    return None


def get_lyric(title, artist):
    track_request_url = 'http://api.musixmatch.com/ws/1.1/track.search'
    track_request_params = {'apikey': API_KEY,
                            'q_track': title, 'q_artist': artist}
    track_response = requests.get(
        track_request_url, params=track_request_params)
    track_info = track_response.json()
    # TODO:エラーハンドリング
    if track_info["message"]["header"]["status_code"] != 200:
        return None
    if len(track_info["message"]["body"]["track_list"]) == 0:
        return None
    # print(track_info)
    track_id = track_info["message"]["body"]["track_list"][0]["track"]["track_id"]

    lyric_request_url = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get'
    lyric_request_params = {'apikey': API_KEY, 'track_id': track_id}
    lyric_response = requests.get(lyric_request_url, lyric_request_params)
    # TODO:エラーハンドリング
    lyric_info = lyric_response.json()
    if lyric_info["message"]["header"]["status_code"] != 200:
        return None
    lyric = lyric_info["message"]["body"]["lyrics"]["lyrics_body"]

    return lyric


def get_line_splitlyric2(title, artist):
    lyric = get_lyric2(title, artist)
    if lyric is None:
        return None

    lyric_section_div = re.split('\n\n', lyric)
    if len(lyric_section_div) == 1:
        lyric_section_div = re.split('\n \n', lyric)

    if len(lyric_section_div) <= 1:
        return [lyric]

    # MUST：有料APIにしたら削除する(無料枠ではここまでと文字が出力されているため)
    lyric_section_div.pop(-1)
    return lyric_section_div


def get_line_splitlyric(title, artist):
    lyric = get_lyric(title, artist)
    if lyric is None:
        return None

    lyric_section_div = re.split('\n\n', lyric)

    # MUST：有料APIにしたら削除する(無料枠ではここまでと文字が出力されているため)
    lyric_section_div.pop(-1)
    return lyric_section_div


def get_formated_lyric(title, path, artist):
    lyric_section_div = get_line_splitlyric2(title, path)
    if lyric_section_div is None:
        lyric_section_div = get_line_splitlyric(title, artist)
        if lyric_section_div is None:
            return None
    lyric_sp = [[] for i in range(len(lyric_section_div))]
    for i in range(len(lyric_section_div)):
        lyric_sp[i] = lyric_section_div[i].replace('.', ' ').split()
    # MUST：有料APIにしたら削除する(無料枠ではここまでと文字が出力されているため)
    if len(lyric_sp) > 1:
        lyric_sp.pop(-1)
    return lyric_sp
