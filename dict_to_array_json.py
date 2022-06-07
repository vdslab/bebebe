import json

path = './test/test_cut_ver.json'
analysis_song_data = []
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for v in data.values():
        print("key,", v)
        analysis_song_data.append(v)

print(len(analysis_song_data))

with open('./test/tiktok.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_song_data, f, indent=2, ensure_ascii=False)
