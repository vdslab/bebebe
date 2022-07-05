from pykakasi import kakasi
import re
import copy
import MeCab

tagger_chasen = MeCab.Tagger('-Ochasen')
tagger_wakachi = MeCab.Tagger('-Owakati')

with open("../../lyrics/tiktok/Habit.txt", "r", encoding="utf-8") as f:
    data = f.read()

data_section_div = re.split('\n\n', data)
data_sp = [[] for i in range(len(data_section_div))]
for i in range(len(data_section_div)):
    data_sp[i] = data_section_div[i].replace('.', ' ').split()

kakasi = kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')

conv = kakasi.getConverter()

vowel_data = copy.deepcopy(data_sp)

# 母音だけに
# for line in vowel_data:
#     for i in range(len(line)):
#         line[i] = re.sub(r"[^aeiou]+", "", conv.do(line[i]))

# 英単語はそのまま, 日本語は母音だけに
vowel_data = [[] for i in range(len(data_section_div))]
for i in range(len(data_section_div)):
    for line in data_section_div[i].split():
        line_wakachi = tagger_wakachi.parse(line).split()
        line_vowel = ""
        for word in line_wakachi:
            isEnglish = re.compile(r'^[a-zA-Z]+$').match(word) is not None
            if isEnglish:
                line_vowel += word
            else:
                line_vowel += re.sub(r"[^aeiou]+", "", conv.do(word))
        vowel_data[i].append(line_vowel)


# vowel_dataのインデックスで母音変換前のdataが分かるように辞書作成。
dic = [[] for i in range(len(data_sp))]
for i in range(len(data_sp)):
    dic[i] = {k: v for k, v in enumerate(data_sp[i])}


# 後ろから何文字の母音が一致しているかを返す
def make_score(word_a, word_b):
    score = 0
    for i in range(min(len(word_a), len(word_b))):
        if word_a == "you":
            print(i, word_a[-1*(i+1)], word_b[-1*(i+1)],
                  word_a[-1*(i+1)] == word_b[-1*(i+1)])
        if word_a[-1*(i+1)] == word_b[-1*(i+1)]:
            score += 1
        else:
            break
    return score

# 母音のみにしたデータと任意の言葉を渡し、元の言葉が分かるようにインデックスとスコアをセットで取得。


def get_idx_score(vowel_data, target_word):
    ranking = []
    for i, word_b in enumerate(vowel_data):
        score = make_score(target_word, word_b)
        ranking.append([i, score])
    return sorted(ranking, key=lambda x: -x[1])


count = 0

for i in range(len(vowel_data)):
    for j in range(len(vowel_data[i])):
        target_word = vowel_data[i][j]
        empty_array = [[] for i in range(j+1)]
        pass_vowel_data = empty_array + vowel_data[i][j+1:]
        # print("--------------------")
        # print("target", target_word, data_sp[i][j])
        ranking = get_idx_score(pass_vowel_data, target_word)
        for k in range(len(ranking)):
            idx = ranking[k][0]
            score = ranking[k][1]
            target_same_word = data_sp[i][j][-1*score:]
            same_word = dic[i][idx][-1*score:]
            if score != 0 and target_same_word != same_word:
                # print("..............................")
                # print("score:" + str(score))
                # print("word:" + dic[i][idx])
                # TODO:重さをつけた方がいい気がする
                count += 1

data_len = sum(len(v) for v in data_sp)
print(count)
print(data_len)
print("score:", count/data_len)
