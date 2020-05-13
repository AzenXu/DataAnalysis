import pandas as pd
from pandas import DataFrame
import numpy as np
import tushare as ts
import os

ts.set_token(os.getenv('TUSHARE_TOKEN'))
pro = ts.pro_api()
# 类型声明
df = DataFrame(pro.daily(ts_code='002230.sz', start_date='1900-01-01', end_date='2099-01-01'))
# 持久化
df.to_csv('./xunfei.csv')

# 读文件
df = pd.read_csv('./xunfei.csv')
'''
      Unnamed: 0    ts_code  trade_date  ...   pct_chg        vol        amount
0              0  002230.SZ    20200513  ...   -0.2928  171993.64  5.843896e+05
1              1  002230.SZ    20200512  ...   -1.1291  233205.86  7.947280e+05
'''

# 干掉第一列
# - axis=1列 - 0行
# - inplace -> 修改源数据
df.drop(labels='Unnamed: 0', axis=1, inplace=True)
'''
        ts_code  trade_date   open  ...   pct_chg        vol        amount
0     002230.SZ    20200513  34.15  ...   -0.2928  171993.64  5.843896e+05
1     002230.SZ    20200512  34.60  ...   -1.1291  233205.86  7.947280e+05
2     002230.SZ    20200511  34.78  ...    0.7879  290258.81  1.002119e+06
'''
# 查看列数据类型
df.info()
'''
 #   Column      Non-Null Count  Dtype  
---  ------      --------------  -----  
 0   ts_code     2832 non-null   object 
 1   trade_date  2832 non-null   int64  
'''

# 设置时间类型 - date数据类型变为了int64，可以直接做索引
# df['date'] = pd.to_datetime(df['trade_date'])

# 将date设置为行索引
df.set_index(df['trade_date'], inplace=True)
'''
trade_date                                ...                                   
20200513    002230.SZ    20200513  34.15  ...   -0.2928  171993.64  5.843896e+05
20200512    002230.SZ    20200512  34.60  ...   -1.1291  233205.86  7.947280e+05
'''

print(df)