import json
import csv

# path = './data/tiktok_ranking_data.json'
path_load = './data/analysis_song_data.json'
path_write = './data/analysis_song_data.csv'

set_data = set()
duplicate_data = []
with open(path_load, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for song_data in data:
        set_data.add(song_data['title'])
    for song_data in data:
        if(song_data['title'] in set_data):
            duplicate_data.append(song_data)
            set_data.remove(song_data['title'])

with open(path_write, 'w') as f:
  json_key_name = ['danceability', 'energy', 'loudness',  'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms','title','ranking']
  writer = csv.writer(f)
  writer.writerow(json_key_name)
  for song_data in duplicate_data:
    writer.writerow([song_data[key] for key in json_key_name])
print(len(set_data))
