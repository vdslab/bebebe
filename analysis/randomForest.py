from sklearn.metrics import mean_squared_error  # RMSE
from sklearn.metrics import r2_score            # 決定係数
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# データセット（train.csvを利用）
df_tiktok = pd.read_json("../data/tiktok.json")
df_spotify = pd.read_json("../data/spotify_150_200_or_over_20500.json")
# df_spotify = pd.read_json("../data/spotify_100_200_tiktok_rm_data.json")
# df_spotify = df_spotify.sample(n=87)
df = pd.concat([df_tiktok, df_spotify])


# df_tiktok = pd.read_json("../data/multipleTiktokData.json")
# df_spotify = pd.read_json("../data/spotify_100_200_tiktok_rm_data.json")
# df = pd.concat([df_tiktok, df_spotify])

# tiktokランキングに入っているものが1, その他0


def ranking_convert(x):
    if x <= 20:
        return 1
    else:
        return 0


def genres_vonvert(x):
    # print(x)
    # if len(x) > 0 and x[0] == "j-pop":
    if "j-rock" in x:
        return 1
    else:
        return 0


# 列にNaNがある行を削除する
df.dropna(subset=['danceability'], axis=0, inplace=True)
# print(df.isnull().sum())

# ランキングを01で
df["ranking"] = df["ranking"].apply(ranking_convert)
# df["genres"] = df["genres"].apply(genres_vonvert)
# df = df[df['genres'] != 0]

df = df.drop('genres', axis=1)

# print(df['ranking'].value_counts())
# print("genres")
# print(df['genres'].value_counts())

"""
# 標準化インスタンス (平均=0, 標準偏差=1)
standard_sc = StandardScaler()

# 01じゃないものを標準化
X = df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness",
               "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]]
X = standard_sc.fit_transform(X)

# 標準化後のデータ出力
df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
           "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]] = X

# print(df.head(3))

# 説明変数
X = df[["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
        "instrumentalness", "liveness", "key", "valence", "time_signature"]]
# "tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"

# 目的変数
y = df["ranking"]

"""

X = df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
               "instrumentalness", "liveness", "key", "valence", "time_signature"]].values
y = df["ranking"]


# トレーニングデータおよびテストデータ分割
X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.4,  random_state=1)


# ランダムフォレスト回帰
forest = RandomForestRegressor(n_estimators=100,
                               criterion='mse',
                               max_depth=None,
                               min_samples_split=2,
                               min_samples_leaf=1,
                               min_weight_fraction_leaf=0.0,
                               max_features='auto',
                               max_leaf_nodes=None,
                               min_impurity_decrease=0.0,
                               bootstrap=True,
                               oob_score=False,
                               n_jobs=None,
                               random_state=None,
                               verbose=0,
                               warm_start=False,
                               ccp_alpha=0.0,
                               max_samples=None
                               )
# モデル学習
forest.fit(X_train, Y_train)

# 推論
y_train_pred = forest.predict(X_train)
y_test_pred = forest.predict(X_test)


""" グラフ可視化 """
"""
# flatten：1次元の配列を返す、argsort：ソート後のインデックスを返す
sort_idx = X_train.flatten().argsort()

# 可視化用に加工
X_train_plot = X_train[sort_idx]
Y_train_plot = Y_train[sort_idx]
train_predict = forest.predict(X_train_plot)

# 可視化
plt.scatter(X_train_plot, Y_train_plot,
            color='lightgray', s=70, label='Traning Data')
plt.plot(X_train_plot, train_predict, color='blue',
         lw=2, label="Random Forest Regression")

# グラフの書式設定
plt.xlabel('LSTAT（低所得者の割合）')
plt.ylabel('MEDV（住宅価格の中央値）')
plt.legend(loc='upper right')
plt.show()
"""


# 平均平方二乗誤差(RMSE)
print('RMSE 学習: %.2f, テスト: %.2f' % (
    mean_squared_error(Y_train, y_train_pred, squared=False),  # 学習
    mean_squared_error(Y_test, y_test_pred, squared=False)    # テスト
))

# 決定係数(R^2)
print('R^2 学習: %.2f, テスト: %.2f' % (
    r2_score(Y_train, y_train_pred),  # 学習
    r2_score(Y_test, y_test_pred)    # テスト
))


# print(Y_test)
# print(y_test_pred)
