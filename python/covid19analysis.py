import numpy as np
import pandas as pd
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

#githubからcsv取得
summary = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/summary.csv') #copyright TOYO KEIZAI ONLINE
#prefectures = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/prefectures.csv') #copyright TOYO KEIZAI ONLINE
#prefectures2 = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/prefectures-2.csv') #copyright TOYO KEIZAI ONLINE
#demography = pd.read_csv('https://github.com/kaz-ogiwara/covid19/raw/master/data/demography.csv') #copyright TOYO KEIZAI ONLINE

#diff時のエラー処理のため文字列の列を抽出しリスト化
obj_pick = summary.select_dtypes(include=object)
index_list = list(obj_pick.columns)
#抽出した列を数値に変換
for i in index_list:
    summary[i] = pd.to_numeric(summary[i] , errors = 'coerce')

#check用コメントアウト
#print(summary.dtypes)
#print(summary.isnull().any())

summary_diff = summary.diff() #日差分データ
summary_diff3 = summary.diff(3) #3日差分データ
summary_diff7 = summary.diff(7) #7日差分データ

#datetime型のindex追加
summary['yymmdd'] = summary['年'].astype(str) + '-' + summary['月'].astype(str) + '-' + summary['日'].astype(str)
summary['yymmdd'] = pd.to_datetime(summary['yymmdd'])
#summary = summary.set_index('yymmdd')
summary_diff['yymmdd'] = summary['yymmdd']
summary_diff3['yymmdd'] = summary['yymmdd']
summary_diff7['yymmdd'] = summary['yymmdd']

#列のインデックス(行は年月日)
#年,月,日,PCR検査陽性者,PCR検査実施人数,有症状者,無症状者,症状有無確認中,入院治療を要する者,入院治療を要する者（無症状）,退院者,退院者（突合作業中を含む）,人工呼吸器又は集中治療室に入院している者,死亡者,死亡者（突合作業中を含む）,PCR検査数：国立感染症研究所,PCR検査数：検疫所,PCR検査数：地方衛生研究所・保健所,PCR検査数：民間検査会社,PCR検査数：民間検査会社のうち保険適用分,PCR検査数：大学等,PCR検査数：大学等のうち保険適用分,PCR検査数：医療機関,PCR検査数：医療機関のうち保険適用分,PCR検査数：合計,PCR検査数：保険適用分の合計,URL

#解析用dataframe作成
plt.figure() #plot initializing
#陽性/PCR人数 1日差分だと誤差大のため7日平均で確認
#summary_diff['yosei/PCR_day'] = summary_diff['PCR検査陽性者'] / summary_diff['PCR検査実施人数']
#summary_diff.plot(x = 'yymmdd', y = 'yosei/PCR_day' , kind='line')
#summary_diff3['yosei/PCR_3day'] = summary_diff3['PCR検査陽性者'] / summary_diff3['PCR検査実施人数']
#summary_diff3.plot(x = 'yymmdd', y = 'yosei/PCR_3day' , kind='line')
summary_diff7['yosei/PCR_7day'] = summary_diff7['PCR検査陽性者'] / summary_diff7['PCR検査実施人数']
summary_diff7.plot(x = 'yymmdd', y = 'yosei/PCR_7day' , kind='line')

#重症病床率＝重病/(入院-退院-死亡)
summary_diff['jusho/nyuin_all_now'] = summary['人工呼吸器又は集中治療室に入院している者'] / (summary['入院治療を要する者'] - summary['退院者'] - summary['死亡者'])
summary_diff.plot(x = 'yymmdd', y = 'jusho/nyuin_all_now' , kind='line')

plt.show()
#参考；大阪独自基準0感染者先週比1.0以下・1感染経路不明10人未満・2陽性率7％未満・3重度病床使用率60％未満
#0陽性/PCR人数・1検査数/検査人数・2重症/(入院-退院-死亡)