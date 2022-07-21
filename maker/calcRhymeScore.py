from pykakasi import kakasi
import re
import copy
import MeCab
import math

tagger_chasen = MeCab.Tagger('-Ochasen')
tagger_wakachi = MeCab.Tagger('-Owakati')
kakasi = kakasi()

# 後ろから何文字の母音が一致しているかを返す


def make_score(word_a, word_b):
    score = 0
    for i in range(min(len(word_a), len(word_b))):
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


def calc_section_rhyme_score(section):
    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')
    conv = kakasi.getConverter()

    data_len = len(section)
    vowel_data = copy.deepcopy(section)

    # 英単語はそのまま, 日本語は母音だけに

    vowel_data = []
    engCount = 0
    wordCount = 0
    isAllEnglish = False
    for line in section:
        line_wakachi = tagger_wakachi.parse(line).split()
        line_vowel = ""
        for word in line_wakachi:
            isEnglish = re.compile(
                r'^[a-zA-Z]+$').match(word) is not None
            isSymbol = re.compile(
                '[0-9!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％—]').match(word) is not None
            if isEnglish:
                line_vowel += word
                engCount += 1
            else:
                line_vowel += re.sub(r"[^aeiou]+", "", conv.do(word))
                if isSymbol:
                    engCount += 1
            wordCount += 1
        vowel_data.append(line_vowel)

    isAllEnglish = engCount == wordCount

    # vowel_dataのインデックスで母音変換前のdataが分かるように辞書作成。
    dic = {k: v for k, v in enumerate(section)}

    count = 0
    isError = False

    for i in range(len(section)):
        target_word = vowel_data[i]
        empty_array = [[] for i in range(i+1)]
        pass_vowel_data = empty_array + vowel_data[i+1:]
        ranking = get_idx_score(pass_vowel_data, target_word)

        # MUST:エラーの原因解明
        if len(pass_vowel_data) != len(section):
            isError = True
            continue

        for k in range(len(ranking)):
            idx = ranking[k][0]
            score = ranking[k][1]
            target_same_word = section[i][-1*score:]
            same_word = dic[idx][-1*score:]
            if score != 0 and target_same_word != same_word:
                # TODO:重さをつけた方がいい気がする
                if score == 1:
                    count += 0.01
                else:
                    count += 1
    # TODO:isErrorの削除
    # TODO:正規化
    if isAllEnglish or isError:
        return None
    else:
        return math.floor(count/data_len*100)


# TODO:この関数の削除かリファクタ
def calc_rhyme_score(data_section_div):
    data_sp = [[] for i in range(len(data_section_div))]
    for i in range(len(data_section_div)):
        data_sp[i] = data_section_div[i].replace('.', ' ').split()

    data_len = sum(len(v) for v in data_sp)

    if data_len == 0:
        exit()

    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')

    conv = kakasi.getConverter()

    vowel_data = copy.deepcopy(data_sp)

    # 英単語はそのまま, 日本語は母音だけに

    vowel_data = [[] for i in range(len(data_section_div))]
    engCount = 0
    wordCount = 0
    isAllEnglish = False
    for i in range(len(data_section_div)):
        for line in data_section_div[i].split():
            line_wakachi = tagger_wakachi.parse(line).split()
            line_vowel = ""
            for word in line_wakachi:
                isEnglish = re.compile(
                    r'^[a-zA-Z]+$').match(word) is not None
                isSymbol = re.compile(
                    '[0-9!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％—]').match(word) is not None
                if isEnglish:
                    line_vowel += word
                    engCount += 1
                else:
                    line_vowel += re.sub(r"[^aeiou]+", "", conv.do(word))
                    if isSymbol:
                        engCount += 1
                wordCount += 1
            vowel_data[i].append(line_vowel)

    isAllEnglish = engCount == wordCount

    # vowel_dataのインデックスで母音変換前のdataが分かるように辞書作成。
    dic = [[] for i in range(len(data_sp))]
    for i in range(len(data_sp)):
        dic[i] = {k: v for k, v in enumerate(data_sp[i])}

    count = 0
    isError = False
    for i in range(len(vowel_data)):
        for j in range(len(vowel_data[i])):
            target_word = vowel_data[i][j]
            empty_array = [[] for i in range(j+1)]
            pass_vowel_data = empty_array + vowel_data[i][j+1:]
            ranking = get_idx_score(pass_vowel_data, target_word)

            # MUST:エラーの原因解明
            if len(pass_vowel_data) != len(data_sp[i]):
                isError = True
                continue

            for k in range(len(ranking)):
                idx = ranking[k][0]
                score = ranking[k][1]
                target_same_word = data_sp[i][j][-1*score:]
                same_word = dic[i][idx][-1*score:]
                if score != 0 and target_same_word != same_word:
                    # TODO:重さをつけた方がいい気がする
                    if score == 1:
                        count += 0.01
                    else:
                        count += 1
    # TODO:isErrorの削除
    return({"value": count/data_len, "isEnglishSong": isAllEnglish, "isError": isError})
