import easyquotation


def quotation_basic_bar():
    # 选择行情 - 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    quotation = easyquotation.use('sina')

    # 获取所有股票行情
    # prefix: 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
    all_bars = quotation.market_snapshot(prefix=False)
    print(all_bars)
    '''
    '000001': {'name': '上证指数', 'open': 3376.4402, 'close': 3367.9658, 'now': 3371.0011, 'high': 3390.5593, 'low': 3352.5017, 'buy': 0.0, 'sell': 0.0, 'turnover': 269562222, 'volume': 377507238826.0, 'bid1_volume': 0, 'bid1': 0.0, 'bid2_volume': 0, 'bid2': 0.0, 'bid3_volume': 0, 'bid3': 0.0, 'bid4_volume': 0, 'bid4': 0.0, 'bid5_volume': 0, 'bid5': 0.0, 'ask1_volume': 0, 'ask1': 0.0, 'ask2_volume': 0, 'ask2': 0.0, 'ask3_volume': 0, 'ask3': 0.0, 'ask4_volume': 0, 'ask4': 0.0, 'ask5_volume': 0, 'ask5': 0.0, 'date': '2020-08-04', 'time': '11:35:03'}
    '''
    '''
        {'sh000159': {'name': '国际实业', # 股票名
          'buy': 8.87, # 竞买价
          'sell': 8.88, # 竞卖价
          'now': 8.88, # 现价
          'open': 8.99, # 开盘价
          'close': 8.96, # 昨日收盘价
          'high': 9.15, # 今日最高价
          'low': 8.83, # 今日最低价
          'turnover': 22545048, # 交易股数
          'volume': 202704887.74， # 交易金额
          'ask1': 8.88, # 卖一价
          'ask1_volume': 111900, # 卖一量
          'ask2': 8.89,
          'ask2_volume': 54700,
          'bid1': 8.87, # 买一价
          'bid1_volume': 21800, # 买一量
          ...
          'bid2': 8.86, 
          'bid2_volume': 78400,
          'date': '2016-02-19',
          'time': '14:30:00',
          ...},
          ......
        }
    '''

    # 单支股票
    bar = quotation.real('162411')  # 支持直接指定前缀，如 'sh000001'

    # 多支股票
    bars = quotation.stocks(['000001', '162411'])

    # 同时获取指数和行情
    index_and_stock = quotation.stocks(['sh000001', 'sz000001'], prefix=True)


# 分时图
def quotation_timekline():
    quotation = easyquotation.use('timekline')
    data = quotation.real(['603828'], prefix=True)
    '''
    :return
    {
       'sh603828': {
            'date': '170721',  #日期 
            'time_data': {
                '201707210930': ['0930', '19.42', '61'], # [时间, 当前价, 上一分钟到这一分钟之间的成交数量]
                '201707210931': ['0931', '19.42','122'], 
                '201707210932': ['0932', '19.43', '123'], 
                '201707210933': ['0933', '19.48', '125'], 
                '201707210934': ['0934', '19.49', '133'], 
                '201707210935': ['0935', '19.48', '161'], 
                ...
        }
    }
    '''
    print(data)


if __name__ == '__main__':
    quotation_basic_bar()
    # quotation_timekline()
