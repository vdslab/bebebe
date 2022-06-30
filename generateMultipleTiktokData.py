from tkinter.tix import ROW
from turtle import title
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import csv
import glob

artist_json_open = open('./data/artist.json', 'r')
artist_name_id_list = json.load(artist_json_open)

client_id = '90e8ab1241af4266a8e5f8306e6e0ed8'
client_secret = '5bc6cff145684388ba4c21962f6b7e38'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret), requests_timeout=5)
json_key_name = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

analysis_song_data = []
file_list = ["./test_data/misato/tiktok_ranking_data_fill_in_the_null.json"]
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for song in data["tiktok_ranking_data"]:
            if song["url"] is None:
                # analysis_song_data[song["title"]] = {}
                continue
            id = song["url"][31:]
            rank = song['ranking']
            date = song['date']
            print(id)
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

            if len(artist_info_list) == 0:
                # print(artist_name_id_list[song["artist"]])
                artist = sp.artist(artist_name_id_list[song["artist"]])
                artist_info_list.append(artist)
                analysis_song_info["artist"] = artist["name"]

            if len(artist_info_list) > 0:
                analysis_song_info["genres"] = artist_info_list[0]["genres"]
                analysis_song_info["artist_uri"] = artist_info_list[0]["uri"][15:]

            # 1番目だけを取るかどうするかどうするか 今は一番目だけ取ってる
            # for artist_info in artist_info_list:
            #     analysis_song_data["genres"].append(artist_info["genres"])

            #analysis_song_data[id] = analysis_song_info
            analysis_song_data.append(analysis_song_info)
            print("ok")

        print(" fin")


print(len(analysis_song_data))

with open('./test/multipleTiktokData.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)

print("all ok")
