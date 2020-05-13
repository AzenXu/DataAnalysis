import pandas as pd
from pandas import DataFrame
import numpy as np
import tushare as ts
import os

def init():
    ts.set_token(os.getenv('TUSHARE_TOKEN'))

def load_data(stock_code: str) -> DataFrame:
    pro = ts.pro_api()
    # 类型声明
    df = DataFrame(pro.daily(ts_code=stock_code, start_date='1900-01-01', end_date='2099-01-01'))
    # 持久化
    df.to_csv('./stock_data.csv')
    # 读文件
    df = pd.read_csv('./stock_data.csv')
    '''
          Unnamed: 0    ts_code  trade_date  ...   pct_chg        vol        amount
    0              0  002230.SZ    20200513  ...   -0.2928  171993.64  5.843896e+05
    1              1  002230.SZ    20200512  ...   -1.1291  233205.86  7.947280e+05
    '''
    return df

def data_clear(df: DataFrame):
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

    # 将date设置为行索引 - 原来是隐式索引012...
    df.set_index(df['trade_date'], inplace=True)
    '''
    trade_date                                ...                                   
    20200513    002230.SZ    20200513  34.15  ...   -0.2928  171993.64  5.843896e+05
    20200512    002230.SZ    20200512  34.60  ...   -1.1291  233205.86  7.947280e+05
    '''


'''
    # 需求一：输出该股票所有：收盘close 比开盘open 上涨3%以上 的日期（拿到行索引即可）
    # (收盘 - 开盘) / 开盘 > 0.03
    # (df['close'] - df['open']) / df['open'] > 0.03  -> 返回Serial(BOOL)类型 -> 将True所对应日期获取出来即可

    # 知识点：在数据分析的过程中，一旦产生了一组BOOL，下一步马上将BOOL作为元数据的行索引取数据 - True对应的取，False对应的不取
    # filter_data = df.head(2).loc[[True, False]]
    # print(df.head(2))
                  ts_code  trade_date   open  ...  pct_chg        vol      amount
    trade_date                                ...                                
    20200513    002230.SZ    20200513  34.15  ...  -0.2928  171993.64  584389.591
    20200512    002230.SZ    20200512  34.60  ...  -1.1291  233205.86  794727.965

    # print(filter_data)
    仅取了True对应的行 - 第一行
                  ts_code  trade_date   open  ...  pct_chg        vol      amount
    trade_date                                ...                                
    20200513    002230.SZ    20200513  34.15  ...  -0.2928  171993.64  584389.591
'''
def load_3_percent_date(df: DataFrame) -> DataFrame:
    # 数据是否满足条件
    condition_serial = (df['close'] - df['open']) / df['open'] > 0.03
    # 通过Serial（True）拿数据
    result = df.loc[condition_serial]
    # 拿到满足要求的行数据的行索引
    result_date = result.index
    return result_date

if __name__ == '__main__':
    init()
    df = load_data('002230.sz')
    data_clear(df)
    dates = load_3_percent_date(df)
    print(dates)





