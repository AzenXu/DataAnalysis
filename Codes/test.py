import pandas as pd
from pandas import DataFrame, Series
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

def data_clear(ori_df: DataFrame):
    # 干掉第一列
    # - axis=1列 - 0行
    # - inplace -> 修改源数据
    ori_df.drop(labels='Unnamed: 0', axis=1, inplace=True)
    '''
            ts_code  trade_date   open  ...   pct_chg        vol        amount
    0     002230.SZ    20200513  34.15  ...   -0.2928  171993.64  5.843896e+05
    1     002230.SZ    20200512  34.60  ...   -1.1291  233205.86  7.947280e+05
    2     002230.SZ    20200511  34.78  ...    0.7879  290258.81  1.002119e+06
    '''
    # 查看列数据类型
    ori_df.info()
    '''
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   ts_code     2832 non-null   object 
     1   trade_date  2832 non-null   int64  
    '''

    # 设置时间类型列
    # def date_change_demo():
    #     # 1，string变成datetime格式
    #     dates = pd.to_datetime(pd.Series(['20010101', '20010331']), format='%Y%m%d')
    #     # # 2，datetime变回string格式
    #     # dates.apply(lambda x: x.strftime('%Y-%m-%d'))
    ori_df['date'] = pd.to_datetime(ori_df['trade_date'], format='%Y%m%d')

    # 将date设置为行索引 - 原来是隐式索引0、1、2...
    ori_df.set_index(ori_df['date'], inplace=True)


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
def load_condition_date(ori_df: DataFrame, condition_serial: Series) -> DataFrame:
    # 通过Serial（True）拿数据
    result = ori_df.loc[condition_serial]
    # 拿到满足要求的行数据的行索引 - 即Date
    result_date = result.index
    return result_date

def load_3_percent_date(ori_df: DataFrame) -> DataFrame:
    # 数据是否满足条件
    condition_serial = (ori_df['close'] - ori_df['open']) / ori_df['open'] > 0.03
    return load_condition_date(ori_df, condition_serial)

'''
需求三：输出该股票所有开盘比*前日*收盘跌幅超过2%的日期
'''
def load_down_2_percent_date(ori_df: DataFrame) -> DataFrame:
    # 数据上移一位 -> shift函数
    # new_df = ori_df.copy()
    # new_df['last_close'] = ori_df['close'].shift(-1) -> 这样写报错...可能是因为NaN那个值导致的
    condition_serial = (ori_df['open'] - ori_df['close'].shift(-1)) / ori_df['close'].shift(-1) < -0.02
    return load_condition_date(ori_df, condition_serial)

'''
需求四：月初定投、年末卖出策略，收益回测
'''
def calculate_income(ori_df: DataFrame):
    # 分析：
    # 1. 将数据从2010年切分到昨天 df['2010':'2020'] - 因为行索引是datetime，故可以直接通过这种方式切片对应时间数据 - 碉堡了
    #       想切月的话 df['2020-05':'2020-01]
    needed_df = ori_df['2020':'2010']
    # 2. 买股票的操作 - 每月第一个交易日买
    #       一个完整的年，需要买12手股票，1200张股票
    #       用开盘价买入

    #   拿每个月第一个交易日对应的行数句
    needed_df_monthly = needed_df.resample('M').first() # resample函数根据条件，对数据重新取样 - 'M': 取每个月 .first: 取第一条数据
    #   计算总花费
    cost = needed_df_monthly['open'].sum() * 100

    # 3. 卖股票的操作 - 每年最后一个交易日
    #       1次卖1200张股票
    #       特殊情况 - 2020年不是一个完整的年，该年还没到最后一个交易日，2020只能买不能卖
    #               - 计算总收益，需要将手里剩余股票的*实际价值*算到总收益中

    #   拿每年最后一个交易日的开盘价 - 剔除掉2020年
    needed_df_yearly = needed_df['2019':'2010'].resample('Y').last()
    benefit_done = needed_df_yearly['open'].sum() * 1200
    #   将20年剩余股票的实际价值计算进来 - 用昨天的收盘价算 * 一共买了5个月 * 100股/手
    benefit_doing =needed_df['close'][0] * 5 * 100
    return benefit_doing + benefit_done - cost


if __name__ == '__main__':
    init()
    df = load_data('002230.sz')
    data_clear(df)

    # 需求二：上升3%
    dates_up_3 = load_3_percent_date(df)
    # 需求三：比前日下降2%
    dates_down_2 = load_down_2_percent_date(df)
    # 需求四：加入从2010年1月1日开始，每月第1个交易日买入1手，每年最后一个交易日卖出所有股票。问：到今天为止，收益是多少？
    income = calculate_income(df)
    print(income)





