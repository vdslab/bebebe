import json

path_spotify = './data/spotify_100_200_data.json'
path_tiktok = "./data/tiktok_dict.json"

analysis_song_data = []

with open(path_spotify, 'r', encoding='utf-8') as f:
    data_spotify = json.load(f)
    with open(path_tiktok, 'r', encoding='utf-8') as f:
        data_tiktok = json.load(f)
        for d in data_spotify:
            if data_tiktok.get(d["id"]) is None:
                analysis_song_data.append(d)

print(len(analysis_song_data))

with open('./test/sample.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)
