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

# データセット（train.csvを利用）
df_tiktok = pd.read_json("../data/tiktok.json")
df_spotify = pd.read_json("../data/spotify_100_200_data.json")
df = pd.concat([df_tiktok, df_spotify])

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
#df["genres"] = df["genres"].apply(genres_vonvert)
#df = df[df['genres'] != 0]
print(df['ranking'].value_counts())
print("genres")
print(df['genres'].value_counts())

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
#"tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness", "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"

# 目的変数
y = df["ranking"]


# トレーニングデータおよびテストデータ分割
X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.3, shuffle=True, random_state=3)


# ロジスティック回帰のインスタンス
model = LogisticRegression(penalty='l2',          # 正則化項(L1正則化 or L2正則化が選択可能)
                           dual=False,            # Dual or primal
                           tol=0.0001,            # 計算を停止するための基準値
                           C=1.0,                 # 正則化の強さ
                           fit_intercept=True,    # バイアス項の計算要否
                           intercept_scaling=1,   # solver=‘liblinear’の際に有効なスケーリング基準値
                           class_weight=None,     # クラスに付与された重み
                           random_state=None,     # 乱数シード
                           solver='lbfgs',        # ハイパーパラメータ探索アルゴリズム
                           max_iter=100,          # 最大イテレーション数
                           multi_class='auto',    # クラスラベルの分類問題（2値問題の場合'auto'を指定）
                           verbose=0,             # liblinearおよびlbfgsがsolverに指定されている場合、冗長性のためにverboseを任意の正の数に設定
                           warm_start=False,      # Trueの場合、モデル学習の初期化に前の呼出情報を利用
                           n_jobs=None,           # 学習時に並列して動かすスレッドの数
                           # L1/L2正則化比率(penaltyでElastic Netを指定した場合のみ)
                           l1_ratio=None
                           )

# モデル学習
model.fit(X_train, Y_train)


df_model = pd.DataFrame(
    index=["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness", "instrumentalness", "liveness", "key", "valence", "time_signature"])
df_model["偏回帰係数"] = model.coef_[0]

print(df_model)
print("intercept: ", model.intercept_)


Y_pred = model.predict(X_test)
print('confusion matrix = \n', confusion_matrix(y_true=Y_test, y_pred=Y_pred))
print('accuracy = ', accuracy_score(y_true=Y_test, y_pred=Y_pred))
print('precision = ', precision_score(y_true=Y_test, y_pred=Y_pred))
print('recall = ', recall_score(y_true=Y_test, y_pred=Y_pred))
print('f1 score = ', f1_score(y_true=Y_test, y_pred=Y_pred))

"""
Y_score = model.predict_proba(X_test)[:, 1]  # 検証データがクラス1に属する確率
fpr, tpr, thresholds = roc_curve(y_true=Y_test, y_score=Y_score)

plt.plot(fpr, tpr, label='roc curve (area = %0.3f)' % auc(fpr, tpr))
plt.plot([0, 1], [0, 1], linestyle='--', label='random')
plt.plot([0, 0, 1], [0, 1, 1], linestyle='--', label='ideal')
plt.legend()
plt.xlabel('false positive rate')
plt.ylabel('true positive rate')
plt.show()
"""
