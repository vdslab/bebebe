import oseti
from janome.tokenizer import Tokenizer
import math

# おせち
analyzer = oseti.Analyzer()
"""
# 極性辞書の作成
dict_polarity = {}
with open('./data/dict/pn_ja.dic.txt', 'r', encoding='shift_jis') as f:
    line = f.read()
    lines = line.split('\n')
    for i in range(len(lines)):
        line_components = lines[i].split(':')
        if len(line_components) >= 4:
            dict_polarity[line_components[0]] = line_components[3]


# ネガポジ分析用の関数の作成(ver2)
# TODO:正規化
def judge_polarity(section):
    t = Tokenizer()
    pol_val = 0
    pos_cnt = 0
    for line in section:
        tokens = t.tokenize(line)
        for token in tokens:
            word = token.surface
            if word in dict_polarity:
                pol_val = pol_val + float(dict_polarity[word])
                pos_cnt += 1
    return pol_val

"""
# おせちでネガポジ分析
# TODO:スコアの算出方法の検討


def oseti_positive_score(section):
    data = " ".join(section)
    result = analyzer.count_polarity(data)
    positive_score = 0
    for res in result:
        posi = res["positive"]
        nega = res["negative"]
        if posi == 0 and nega == 0:
            positive_score += 50
        else:
            positive_score += posi/(posi+nega)*100
    positive_score = None if len(result) == 0 else math.floor(
        positive_score/len(result))
    return positive_score


def calc_section_positive_score(section):
    score = oseti_positive_score(section)

    return score
