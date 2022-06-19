from sklearn.decomposition import PCA  # 主成分分析器
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import plotting


# データセット（train.csvを利用）
df_tiktok = pd.read_json("../data/tiktok.json")
df_spotify = pd.read_json("../data/spotify_187_200_tiktok_rm_data.json")
df = pd.concat([df_tiktok, df_spotify])

#df = pd.read_json("../data/tiktok.json")
#df = pd.read_json("../data/spotify_187_200_tiktok_rm_data.json")
#df = pd.read_json("../data/spotify_100_200_tiktok_rm_data.json")
#df = df.sample(n=87)


# tiktokランキングに入っているものが1, その他0


def ranking_convert(x):
    if x <= 20:
        return 1
    else:
        return 0


def genres_vonvert(x):
    # print(x)
    # if len(x) > 0 and x[0] == "j-pop":
    if "anime" in x:
        return 1
    else:
        return 0


# 列にNaNがある行を削除する
df.dropna(subset=['danceability'], axis=0, inplace=True)
# print(df.isnull().sum())

# ランキングを01で
df["ranking"] = df["ranking"].apply(ranking_convert)
# ジャンルで絞りたいとき
df["genres"] = df["genres"].apply(genres_vonvert)
df = df[df['genres'] != 0]

print(df['ranking'].value_counts())
# print("genres")
# print(df['genres'].value_counts())

# 列を削除
df = df.drop('id', axis=1)
df = df.drop('title', axis=1)
df = df.drop('artist', axis=1)
df = df.drop('date', axis=1)
df = df.drop('artist_uri', axis=1)
df = df.drop('genres', axis=1)

# print(df.head(3))
# print(df.iloc[:, 13])

# それぞれに与える色を決める。
color_codes = {0: 'blue', 1: 'red', 2: '#0000FF'}
# サンプル毎に色を与える。
colors = [color_codes[x] for x in list(df.iloc[:, 13])]

df = df.drop('ranking', axis=1)

# とりあえず散布図
plotting.scatter_matrix(df.iloc[:, 0:], figsize=(
    8, 8), c=colors, alpha=0.5)
plt.show()


# 標準化インスタンス (平均=0, 標準偏差=1)
standard_sc = StandardScaler()

# 01じゃないものを標準化
X = df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness",
               "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]]
X = standard_sc.fit_transform(X)

# 標準化後のデータ出力
df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
           "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]] = X
dfs = df.copy()


# 主成分分析の実行
pca = PCA()
pca.fit(dfs)
# データを主成分空間に写像
feature = pca.transform(dfs)

# print(feature)
print(list(df.iloc[:, 12]))

# 主成分得点
pd.DataFrame(feature, columns=["PC{}".format(x + 1)
             for x in range(len(dfs.columns))]).head()

# 第一主成分と第二主成分でプロットする
plt.figure(figsize=(6, 6))
plt.scatter(feature[:, 0], feature[:, 1], alpha=0.8, c=colors)
plt.grid()
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

plotting.scatter_matrix(pd.DataFrame(feature,
                        columns=["PC{}".format(x + 1) for x in range(len(df.columns))]),
                        figsize=(8, 8), c=colors, alpha=0.5)
plt.show()
