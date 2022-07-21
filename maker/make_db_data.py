import json
import os
from tkinter.tix import ROW
from turtle import title
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from getLyric import get_formated_lyric
from analysisLyric import analysis_lyric

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET_ID')), requests_timeout=5)


#song_list_file = open('../data/spotify_187_200_tiktok_rm_data.json', 'r')
song_list_file = open('../data/tiktok2.json', 'r')
song_list = json.load(song_list_file)

db_song_data = []
db_past_song_data = []

for song in song_list:
    song_data = dict()
    past_song_data = dict()
    song_data["id"] = song["id"]
    song_data["title"] = song["title"]
    # TODO:アーティスト、歌詞データ、が取れるものは取る
    if song["id"] == "":
        continue

    track = sp.track(song["id"])
    if track:
        song_data["preview_url"] = sp.track(song["id"])["preview_url"]
    else:
        song_data["preview_url"] = None
    song_data["artist"] = song["artist"]
    song_data["artist_uri"] = song["artist_uri"]
    song_data["genres"] = song["genres"]

    music_feature = {
        "danceability": song["danceability"],
        "energy": song["energy"],
        "key": song["key"],
        "loudness": song["loudness"],
        "mode": song["mode"],
        "speechiness": song["speechiness"],
        "acousticness": song["acousticness"],
        "instrumentalness": song["instrumentalness"],
        "liveness": song["liveness"],
        "valence": song["valence"],
        "tempo": song["tempo"],
        "duration_ms": song["duration_ms"],
        "time_signature": song["time_signature"],
    }

    # lyric_text = get_formated_lyric(
    #     song["title"], "../lyrics/spotify/all/*", song["artist"])
    lyric_text = get_formated_lyric(
        song["title"], "../lyrics/tiktok/*", song["artist"])

    if lyric_text is None:
        lyrics_feature = None
        print(song["title"])
    else:
        lyrics_feature = analysis_lyric(lyric_text)

    song_data["music_feature"] = music_feature
    song_data["lyrics_feature"] = lyrics_feature

    # past song
    past_song_data["id"] = song["id"]
    past_song_data["date"] = song["date"]
    past_song_data["rank"] = song["ranking"]

    db_song_data.append(song_data)
    db_past_song_data.append(past_song_data)
    # print(song_data)
    print("OK")


with open('./tiktok2_db_song.json', 'w', encoding='utf-8') as f:
    json.dump(db_song_data, f, indent=2, ensure_ascii=False)

with open('./tiktok2_db_past_song.json', 'w', encoding='utf-8') as f:
    json.dump(db_past_song_data, f, indent=2, ensure_ascii=False)

print("all ok")
