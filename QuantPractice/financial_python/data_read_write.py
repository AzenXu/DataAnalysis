import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
    # --- Yahoo源 - 过期了 ---
    # $ pip install pandas-datareader
    # $ pip install yfinance --upgrade --no-cache-dir  - doc:https://pypi.org/project/fix-yahoo-finance/
    # import pandas_datareader
    # import yfinance as yf
    # yf.pdr_override()
    #
    # gs_stock = pandas_datareader.data.get_data_yahoo('GS', start='2020-05-01', end='2020-06-01')
    # # requests.exceptions.SSLError:
    # # SOCKSHTTPSConnectionPool(host='query1.finance.yahoo.com', port=443):
    # # Max retries exceeded with url:
    # # 似乎是接口被封了？不太能用了呢

    # # --- quandl源 ---
    # # pip install quandl
    # # doc: www.quandl.com
    # # 也是炒鸡慢...估计还得报个错，不管它了吧
    # import quandl
    # data = quandl.get('EOD/KO', start_date='2020-1-1', end_date='2020-6-1')
    # print(data)

    import tushare as ts
    import os

    ts.set_token(os.getenv('TUSHARE_TOKEN'))

    # pro = ts.pro_api()
    # df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    # print(df)

    pass


if __name__ == '__main__':
    # local_file_read()
    network_data_read()
    print('I come back again~ ')
