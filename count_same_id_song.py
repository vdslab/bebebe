from operator import truediv
from tkinter.tix import ROW
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import csv
import glob

"""
analysis_song_data = []
with open('./data/tiktok_dict.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    # print(data)
    for id, song in data.items():
        song["count"] = 0

    analysis_song_data = data


with open('./test/test.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)
"""


analysis_song_data = []
count = 0
with open('./data/tiktok_dict.json', 'r', encoding='utf-8') as f:
    dict_data = json.load(f)
    with open('./test_data/sanma/tiktok_ranking_data.json', 'r', encoding='utf-8') as f:
        row_data = json.load(f)
        for rd in row_data["tiktok_ranking_data"]:
            find = False
            for id, song in dict_data.items():
                #print(rd["title"], song["title"], rd["title"] == song["title"])
                if rd["title"] == song["title"]:
                    find = True
                    song["count"] += 1
                    break
            if find:
                count += 1
            else:
                print(rd["title"], "//", song["title"],
                      rd["title"] == song["title"])
        analysis_song_data = dict_data


print(count)


with open('./test/test.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)
