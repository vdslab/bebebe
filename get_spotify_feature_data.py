from tkinter.tix import ROW
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import csv
import glob


artist_json_open = open('./data/artist.json', 'r')
artist_name_id_list = json.load(artist_json_open)

client_id = ''
client_secret = ''

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret), requests_timeout=5)
json_key_name = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

analysis_song_data = dict()
for filename in sorted(glob.glob("../spotify_chart_data/regional-jp-weekly-*.csv")):
    with open(filename, newline="") as f:
        dic_reader = csv.DictReader(f)
        for row in dic_reader:
            id = row["uri"][14:]
            rank = row['\ufeffrank']
            date = filename[-14:-4]
            if int(rank) < 100:
                continue
            song_features = sp.audio_features(id)
            analysis_song_info = dict()
            analysis_song_info['id'] = id
            analysis_song_info['title'] = row['track_name']
            for key in json_key_name:
                analysis_song_info[key] = song_features[0][key]
            analysis_song_info['ranking'] = rank
            analysis_song_info['date'] = date

            # add
            artist_name = row["artist_names"]
            artist_result = sp.search(q='artist:' + artist_name, type='artist')
            artist_info_list = artist_result["artists"]["items"]
            analysis_song_info["artist"] = artist_name

            if len(artist_info_list) == 0:
                print(artist_name_id_list[row["artist_names"]])
                artist = sp.artist(artist_name_id_list[row["artist_names"]])
                artist_info_list.append(artist)
                analysis_song_info["artist"] = artist["name"]

            if len(artist_info_list) > 0:
                analysis_song_info["genres"] = artist_info_list[0]["genres"]
                analysis_song_info["artist_uri"] = artist_info_list[0]["uri"][15:]

            # 1番目だけを取るかどうするかどうするか 今は一番目だけ取ってる
            # for artist_info in artist_info_list:
            #     analysis_song_data["genres"].append(artist_info["genres"])

            analysis_song_data[id] = analysis_song_info
        print(date, " fin")

print(len(analysis_song_data))

with open('./test/analysis-song-data-100-200.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)

print("all ok")
