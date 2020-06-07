import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts
import os


def local_file_read():
    with open('./demo_data/person_ability.csv', 'r') as file:
        print(file.read())
    """
    人物,内力,刀法,剑法,暗器,拳掌,
    张楚岚,10,7,2,2,5,
    王也,2,3,8,9,9,
    诸葛青,6,1,3,3,9,
    冯宝宝,1,10,4,9,9,
    """

    import csv
    csv_reader = csv.reader(open('./demo_data/person_ability.csv', 'r'))
    data = [i for i in csv_reader]
    print(data[:3])
    """
    [['人物', '内力', '刀法', '剑法', '暗器', '拳掌', ''],
     ['张楚岚', '10', '7', '2', '2', '5', ''],
      ['王也', '2', '3', '8', '9', '9', '']]
    """

    data = pd.read_csv('./demo_data/person_ability.csv',
                       index_col=0,
                       parse_dates=False
                       )
    print(data)
    """
             内力  刀法  剑法  暗器  拳掌  Unnamed: 6
    人物                                 
    张楚岚  10   7   2   2   5         NaN
    王也    2   3   8   9   9         NaN
    诸葛青   6   1   3   3   9         NaN
    冯宝宝   1  10   4   9   9         NaN
    """
    del data['Unnamed: 6']
    data.loc['张楚岚', '拳掌'] = 999
    data.to_csv('./demo_data/person_ability_hacked.csv')
    data.to_json('./demo_data/person_ability_hacked.json')
    print(data)


def network_data_read():
    # # --- Yahoo源 ---
    # # $ pip install pandas-datareader
    # # $ pip install yfinance --upgrade --no-cache-dir  - doc:https://pypi.org/project/fix-yahoo-finance/
    # import pandas_datareader
    # import yfinance as yf
    # yf.pdr_override()
    #
    # gs_stock = pandas_datareader.data.get_data_yahoo('GS', start='2020-05-01', end='2020-06-01')
    # print(gs_stock)
    # """
    #     [*********************100%***********************]  1 of 1 completed
    #                   Open        High         Low       Close   Adj Close   Volume
    # Date
    # 2020-04-30  186.000000  187.550003  182.899994  183.419998  182.280579  2690700
    # 2020-05-01  179.000000  179.600006  176.649994  177.100006  175.999847  2650200
    # """

    # --- quandl源 ---
    # pip install quandl
    # doc: www.quandl.com
    # 需要注册拿个key才能用
    # import quandl
    # data = quandl.get('EOD/KO', start_date='2020-1-1', end_date='2020-6-1')
    # print(data)

    # --- Tushare源 ---
    import tushare as ts
    import os

    ts.set_token(os.getenv('TUSHARE_TOKEN'))
    # df = ts.pro_bar(ts_code='000300.SH', asset='I', start_date='20180101', end_date='20181011')

    df = ts.pro_bar(ts_code='600030.SH',
                    # asset='I',  # *2-1
                    start_date='20200501',
                    end_date='20200601')  # *2-2
    df.set_index('trade_date', inplace=True)
    df.close.plot()
    # plt.show()

    df = ts.pro_bar('600030.SH', freq='M')
    df.head()

    df = ts.pro_api().index_basic()
    """
           ts_code         name market  ... base_date base_point list_date
0    000001.SH         上证指数    SSE  ...  19901219     100.00  19910715
1    000002.SH         上证A指    SSE  ...  19901219     100.00  19920221
2    000003.SH         上证B指    SSE  ...  19920221     100.00  19920221
3    000004.SH      上证工业类指数    SSE  ...  19930430    1358.78  19930503
4    000005.SH      上证商业类指数    SSE  ...  19930430    1358.78  19930503
    """

    pass


def multi_stock_search(codes: list = None):
    if codes is None:
        codes = ['002230.SZ', '603000.SH', '600804.SH']

    ts.set_token(os.getenv('TUSHARE_TOKEN'))

    def multiple_stocks() -> pd.DataFrame:
        def load_stock(code: str):
            print(code)

            # 查沪深300，则把asset设置为I，否则为E
            asset = 'E'
            if code == '000300.SH':
                asset = 'I'

            stock: pd.DataFrame = ts.pro_bar(code, asset=asset, start_date='20200101', end_date='20200601')
            stock.index = pd.to_datetime(stock.trade_date)
            return stock

        # 获取到每个股票的DF
        # map、reduce老熟人 - 函数式里面老用，这里也出现了
        stock_sequence = map(load_stock, codes)  # 1

        # 拼接成一个大DF返回
        return pd.concat(stock_sequence,
                         keys=codes,  # 2
                         names=['Code', 'Date'])  # 3

    stocks = multiple_stocks()

    print(stocks)
    """
                            ts_code   open   high  ...  pct_chg        vol       amount
Code      Date                                 ...                                 
002230.SZ 2020-06-01  002230.SZ  32.20  33.06  ...   3.0986  307341.74  1005989.768
          2020-05-29  002230.SZ  31.51  32.20  ...   0.5982  191645.19   612902.695
          2020-05-28  002230.SZ  31.99  32.26  ...   0.1893  204060.85   648539.201
          2020-05-27  002230.SZ  32.25  32.25  ...  -1.5528  223192.53   708397.163
          2020-05-26  002230.SZ  31.75  32.22  ...   2.0602  196149.12   628701.459
...                         ...    ...    ...  ...      ...        ...          ...
600804.SH 2020-01-08  600804.SH   6.68   6.80  ...  -2.2523  532769.32   353582.714
          2020-01-07  600804.SH   6.60   6.77  ...   1.8349  529362.09   351918.098
          2020-01-06  600804.SH   6.43   6.62  ...   0.6154  413331.87   269603.676
          2020-01-03  600804.SH   6.41   6.52  ...   1.5625  431078.14   277649.217
          2020-01-02  600804.SH   6.17   6.42  ...   4.5752  486907.39   307360.460
    """
    # stocks_close.plot()
    # plt.show()

    return stocks


def get_stocks_close(stocks: pd.DataFrame) -> pd.DataFrame:
    def get_stocks_close_one() -> pd.DataFrame:
        # 法一：利用多重索引的unstack()
        stocks_close = stocks.close.unstack().T.sort_index(ascending=True)
        #     """
        #     Code        002230.SZ  603000.SH  600804.SH
        # Date
        # 2020-06-01      32.94      19.68       7.47
        # 2020-05-29      31.95      19.20       6.79
        # 2020-05-28      31.76      18.82       6.55
        #     """
        return stocks_close

    def get_stocks_close_two() -> pd.DataFrame:
        # 法二：透视图
        # 先把索引重置为position - 原双重索引变为普通column
        stock_normal = stocks.reset_index()
        print(stock_normal)
        """
              Code       Date    ts_code  ... pct_chg        vol       amount
        0    002230.SZ 2020-06-01  002230.SZ  ...  3.0986  307341.74  1005989.768
        1    002230.SZ 2020-05-29  002230.SZ  ...  0.5982  191645.19   612902.695
        """
        stocks_close = stock_normal.pivot(
            index='Date',
            columns='Code',
            values='close'
        )
        """
        Code        002230.SZ  600804.SH  603000.SH
        Date                                       
        2020-01-02      35.04       6.40      20.40
        2020-01-03      34.66       6.50      22.44
        """
        return stocks_close

    return get_stocks_close_one()


# 要画收盘价图 - x轴：时间，y轴：收盘价，legend：code
def close_price_draw(stocks: pd.DataFrame):
    # 需要先把表格搞出来 - index：date，column：code，values：收盘价
    get_stocks_close(stocks).plot()
    plt.show()


def return_ratio_draw(stocks: pd.DataFrame):
    stocks_close = get_stocks_close(stocks)
    return_ratio_1 = stocks_close / stocks_close.shift() - 1
    # 计算与其前一个元素的变化百分比
    return_ratio_2 = stocks_close.pct_change()  # 1-1
    # 计算累计收益率
    cum_return_ratio = (return_ratio_2 + 1).cumprod()
    # 画之
    cum_return_ratio.plot()
    plt.show()


def return_ratio_hist(stocks: pd.DataFrame):
    stocks_return = get_stocks_close(stocks).pct_change()
    stocks_return.hist(bins=60)
    plt.show()


def qq_plot(stocks_return: pd.DataFrame):
    import scipy.stats as stats
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    stats.probplot(
        stocks_return['002230.SZ'],
        dist='norm',
        plot=ax
    )
    plt.show()


def return_correlated():
    # 拿到return表
    stocks_return = get_stocks_close(multi_stock_search(
        ['000300.SH', '002230.SZ', '603000.SH', '600804.SH']
    )).pct_change()
    # stocks_return = stocks_close.pct_change()
    # print(stocks_return)

    # 计算相关性
    stocks_corr = stocks_return.corr()
    print(stocks_corr)

    # 画热力图
    import seaborn
    seaborn.heatmap(stocks_corr, vmin=0)
    plt.show()

    # 两支股相关性研究 - 散点图
    plt.figure(figsize=(8, 6))
    plt.title('科大-HS300相关性')
    plt.plot(stocks_return['000300.SH'], stocks_return['002230.SZ'], '.')
    plt.show()


def datetime_control():
    print('Can I control the TIME?')

    def python_date():
        from datetime import datetime
        # 构建
        now = datetime.now()
        print(
            now,  # 2020-06-05 16:53:41.560043
            type(now),  # <class 'datetime.datetime'>
            '{}年{}月{}日'.format(now.year, now.month, now.day)  # 2020年6月5日
        )

        some_time = datetime(2020, 5, 25, 23, 0)
        print(some_time)  # 2020-05-25 23:00:00

        # 转化 - d to str
        some_time_str = str(some_time)
        print(some_time_str)  # 2020-05-25 23:00:00

        some_time_str2 = some_time.strftime('%d/%m/%Y')  # 25/05/2020
        print(some_time_str2)

        # 转化 - str to d
        # 法1 - 内置
        date_str = '2017-06-18'
        date_real = datetime.strptime(date_str, '%Y-%m-%d')
        print(date_real)
        # 法2 - dateutil
        from dateutil.parser import parse
        date_real2 = parse('01-02-2020', dayfirst=True)
        print(date_real2)  # 2020-02-01 00:00:00
        # 法3 - pandas
        print(pd.to_datetime('20200202'))

    # python_date()

    def date_index():
        from datetime import datetime

        # datetimeindex - 构建一 - pd.DatetimeIndex()
        print(pd.DatetimeIndex([datetime(2020, 6, 7)]))
        # DatetimeIndex(['2020-06-07'], dtype='datetime64[ns]', freq=None)
        print(pd.date_range('20200601', '20200607'))

        # datetimeindex - 构建二 - pd.date_range()
        df = pd.DataFrame(
            np.random.randn(300, 2).round(2),
            index=pd.date_range('20200101', periods=300, freq='D'),
            columns=['天气', '心情']
        )
        print(df)

        # datetimeindex特点1 - 按月切片，不用.loc - 按天还是得.loc
        print(df['2020-01'])

        # datetimeindex特点2 - 从月切到天
        print(df['2020-02':'2020-03-04'])

        pass

    # date_index()

    def date_resample():
        # 注意：单独对TimeSeries重取样没意义，resample是df的对象方法
        date = pd.date_range('20200525', '20200630')

        df = pd.DataFrame(np.random.randn(300, 2),
                          index=pd.date_range('20200525', periods=300)
                          )

        # 此处API有变动，不再支持how参数
        mean_monthly = df.resample('M').mean()
        # 计算每阶段的open、close、high、low
        ohlc_monthly = df.resample('M').ohlc()
        print(ohlc_monthly)

        # 降采样
        # 指定fillna规则 - ffill - 向前填充
        print(df.resample('H').fillna(method='ffill'))
        # 指定fillna规则 - 线性插值
        print(df.resample('H').interpolate())

    # date_resample()

    pass


if __name__ == '__main__':
    # local_file_read()
    # network_data_read()
    # close_price_draw(multi_stock_search())
    # return_ratio_draw(multi_stock_search())
    # return_ratio_hist(multi_stock_search())
    # qq_plot(get_stocks_close(multi_stock_search()).pct_change())
    # return_correlated()

    #  --- 时间部分 ---
    datetime_control()

    # --- 两个Case ---


    print('I come back again~ ')
