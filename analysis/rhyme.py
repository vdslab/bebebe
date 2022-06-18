from pykakasi import kakasi
import re

with open("./analysis/rhyme_word/ブラザービート.txt", "r", encoding="utf-8") as f:
    data = f.read()

data_sp = data.split()
target_word_origin = "ブラザービート"

kakasi = kakasi()

kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')

conv = kakasi.getConverter()

target_word = conv.do(target_word_origin)
text_data = conv.do(data).split()
text_data = list(text_data)

target_word_vo = re.sub(r"[^aeiou]+", "", target_word)
vowel_data = [re.sub(r"[^aeiou]+", "", text) for text in text_data]

dic = {k: v for k, v in enumerate(data_sp)}


def make_score(word_a, word_b):
    score = 0
    if len(word_a) > len(word_b):
        word_len = len(word_b)
        for i in range(word_len):
            for j in range(word_len + 1):
                if word_b[i:j] in word_a:
                    score += len(word_b[i:j])
    else:
        word_len = len(word_a)
        for i in range(word_len):
            for j in range(word_len + 1):
                if word_a[i:j] in word_b:
                    score += len(word_a[i:j])
    return score


def get_idx_score(vowel_data, target_word):
    ranking = []
    for i, word_b in enumerate(vowel_data):
        score = make_score(target_word, word_b)
        ranking.append([i, score])
    return sorted(ranking, key=lambda x: -x[1])


ranking = get_idx_score(vowel_data, target_word_vo)
print(target_word_origin)
for i in range(len(ranking)):
    idx = ranking[i][0]
    score = ranking[i][1]
    print("score:" + str(score))
    print("word:" + dic[idx])
