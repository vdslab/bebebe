
import json
spotify_song_list_file = open('./spotify_db_song.json', 'r')
spotify_song_list = json.load(spotify_song_list_file)
tiktok_song_list_file = open('./tiktok_db_song.json', 'r')
tiktok_song_list = json.load(tiktok_song_list_file)

print(len(spotify_song_list)+len(tiktok_song_list))

db_song_data = set()

for song in spotify_song_list:
    db_song_data.add(song["id"])


for song in tiktok_song_list:
    db_song_data.add(song["id"])

print(len(db_song_data))
