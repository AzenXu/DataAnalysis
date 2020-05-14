import pandas as pd
from pandas import DataFrame
import tushare as ts

class DataLoader:
    def __init__(self):
        print('This is init function')

    @staticmethod
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

    @staticmethod
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