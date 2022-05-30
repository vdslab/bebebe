import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotify_id as sid


client_id = 'your client id'
client_secret = 'your secret id'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret), requests_timeout=5)
json_key_name = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
path = './data/tiktok_ranking_data.json'
analysis_song_data = []
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    tiktok_ranking_data = data['tiktok_ranking_data']
    print(len(tiktok_ranking_data))
    for ranking_data in tiktok_ranking_data:
        if(ranking_data.get('url') == None or ranking_data.get('url') == "404"):
            continue
        analysis_song_info = dict()
        analysis_song_info['url'] = ranking_data['url']
        analysis_song_info['title'] = ranking_data['title']
        song_features = sp.audio_features(ranking_data['url'])
        for key in json_key_name:
            analysis_song_info[key] = song_features[0][key]
        analysis_song_info['ranking'] = ranking_data['ranking']
        analysis_song_info['date'] = ranking_data['date']
        analysis_song_data.append(analysis_song_info)
with open('./data/analysis_song_data.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)
