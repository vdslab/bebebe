import numpy as np
import pandas as pd
from scipy import stats

# t検定とか


# データセット（train.csvを利用）
# df_tiktok = pd.read_json("../data/tiktok.json")
# df_spotify = pd.read_json("../data/spotify_150_200_or_over_20500.json")
#df_spotify = pd.read_json("../data/spotify_187_200_tiktok_rm_data.json")
# df_spotify = pd.read_json("../data/spotify_100_200_tiktok_rm_data.json")
# df_spotify = df_spotify.sample(n=87)


df_tiktok = pd.read_json("../data/multipleTiktokData.json")
df_spotify = pd.read_json("../data/spotify_100_200_tiktok_rm_data.json")


features = ["tempo", "danceability", "energy", "mode", "loudness", "acousticness", "speechiness",
            "instrumentalness", "liveness", "key", "valence", "duration_ms", "time_signature"]


for feature in features:
    print("----------", feature, "---------------")

    test_tiktok = df_tiktok.loc[:, feature].to_numpy()
    # nanを削除
    test_tiktok = test_tiktok[~np.isnan(test_tiktok)]
    test_spotify = df_spotify.loc[:, feature].to_numpy()

    """
    F検定を行う
    """
    tiktok_var = np.var(test_tiktok, ddof=1)  # Aの不偏分散
    spotify_var = np.var(test_spotify, ddof=1)  # Bの不偏分散
    A_df = len(test_tiktok) - 1  # Aの自由度
    B_df = len(test_spotify) - 1  # Bの自由度
    f = tiktok_var / spotify_var  # F比の値
    one_sided_pval1 = stats.f.cdf(f, A_df, B_df)  # 片側検定のp値 1
    one_sided_pval2 = stats.f.sf(f, A_df, B_df)   # 片側検定のp値 2
    two_sided_pval = min(one_sided_pval1, one_sided_pval2) * 2  # 両側検定のp値

    # print('F:       ', round(f, 3))
    # print('p-value: ', round(two_sided_pval, 3))

    f_p_value = round(two_sided_pval, 3)

    if f_p_value > 0.05:
        """
        等分散性がある時, studentのt検定を行う
        """
        res = stats.ttest_ind(test_tiktok, test_spotify)
        print(res.pvalue < 0.05, res)
    else:
        """
        Welchのt検定
        """
        res = stats.ttest_ind(test_tiktok, test_spotify, equal_var=False)
        print(res.pvalue < 0.05, res)
