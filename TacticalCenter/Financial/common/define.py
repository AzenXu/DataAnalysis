import tushare as ts
import os
import numpy as np
import pandas as pd


class Stock:
    def __init__(self, code, name, asset='E'):
        self.code = code
        self.asset = asset
        self.name = name

    def get_bar(self, start_date: str, end_date: str):
        """
        获取行情数据
        :param start_date
        :param end_date
        :return: https://tushare.pro/document/2?doc_id=27
        """
        ts.set_token(os.getenv('TUSHARE_TOKEN'))

        bar: pd.DataFrame = ts.pro_bar(ts_code=self.code, asset=self.asset, adj='qfq', start_date=start_date,
                                       end_date=end_date)
        bar.index = pd.to_datetime(bar['trade_date'])
        bar.sort_index(inplace=True)
        return bar

    def get_cum_returns(self, start_date: str, end_date: str):
        """
        获取累积收益
        :param start_date:
        :param end_date:
        :return:
        """
        return (self.get_bar(start_date, end_date)['close'].pct_change() + 1).cumprod()


xunfei = Stock(code='002230.sz', name='科大讯飞')
mengjie = Stock(code='002397.sz', name='梦洁家纺')  # AQF - Aberration系统用到的DemoStock
zykj = Stock(code='603533.sh', name='掌阅科技')

hs300 = Stock(code='000300.sh', name='沪深300', asset='I')

zz500ETF = Stock(code='510510.sh', name='中证500ETF', asset='FD')
debtETF = Stock(code='511010.sh', name='国债ETF', asset='FD')
