from tkinter.tix import ROW
from turtle import title
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import csv
import glob


client_id = 'your client id'
client_secret = 'your secret id'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret), requests_timeout=5)
json_key_name = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

analysis_song_data = dict()
file_list = ["./test/tiktok_ranking_data_fill_in_the_null.json"]
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for song in data["tiktok_ranking_data"]:
            if song["url"] is None:
                analysis_song_data[song["title"]] = {}
                continue
            id = song["url"][31:]
            rank = song['ranking']
            date = song['date']
            song_features = sp.audio_features(id)
            analysis_song_info = dict()
            analysis_song_info['id'] = id
            analysis_song_info['title'] = song['title']
            for key in json_key_name:
                analysis_song_info[key] = song_features[0][key]
            analysis_song_info['ranking'] = rank
            analysis_song_info['date'] = date

            # add

            artist_name = song["artist"]
            artist_result = sp.search(q='artist:' + artist_name, type='artist')
            artist_info_list = artist_result["artists"]["items"]

            analysis_song_info["artist"] = artist_name
            if len(artist_info_list) > 0:
                analysis_song_info["genres"] = artist_info_list[0]["genres"]
                analysis_song_info["artist_uri"] = artist_info_list[0]["uri"][15:]

            # 1番目だけを取るかどうするかどうするか 今は一番目だけ取ってる
            # for artist_info in artist_info_list:
            #     analysis_song_data["genres"].append(artist_info["genres"])

            analysis_song_data[id] = analysis_song_info
            print(song["title"], "ok")

        print(" fin")


print(len(analysis_song_data))

with open('./test/test.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)

print("all ok")
