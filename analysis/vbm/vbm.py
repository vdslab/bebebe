from tkinter import Y
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

"""重複なし"""
df_tiktok = pd.read_json("data/tiktok.json")
df_spotify = pd.read_json("data/spotify_150_200_or_over_20500.json")
df = pd.concat([df_tiktok, df_spotify])


"""重複あり"""
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


# ランキングを01で
df["ranking"] = df["ranking"].apply(ranking_convert)

# 標準化インスタンス (平均=0, 標準偏差=1)
standard_sc = StandardScaler()

# 01じゃないものを標準化
X = df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness",
               "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]]
X = standard_sc.fit_transform(X)

# 標準化後のデータ出力
df.loc[:, ["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
           "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]] = X


# 説明変数
X = df[["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
        "instrumentalness", "liveness", "key", "valence", "time_signature"]]
# "tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"

# 目的変数
y = df["ranking"]


# トレーニングデータおよびテストデータ分割
X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.5, shuffle=True, random_state=3)


"""以降追加"""

# 線形SVMのインスタンスを生成

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

model = SVC(kernel='linear', random_state=None)
# モデルの学習。fit関数で行う。
model.fit(X_train_std, Y_train)

model = LogisticRegression(random_state=None)


''' # トレーニングデータに対する精度
pred_train = model.predict(X_train_std)
accuracy_train = accuracy_score(Y_train, pred_train)
print('トレーニングデータに対する正解率： %.2f' % accuracy_train)

# テストデータに対する精度
pred_test = model.predict(X_test_std)
accuracy_test = accuracy_score(Y_test, pred_test)
print('テストデータに対する正解率： %.2f' % accuracy_test) '''


import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions
plt.style.use('ggplot') 

X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((Y_train,Y_test))

fig = plt.figure(figsize=(13,8))
plot_decision_regions(X_combined_std, y_combined, clf=model)
plt.show()