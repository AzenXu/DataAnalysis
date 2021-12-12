
# 优矿原文件（未调整） -> https://uqer.datayes.com/labs/notebooks/300p2%E7%BB%9F%E8%AE%A1.nb
# 大部分SDK无法本地调用，需在优矿上运行

# coding: utf-8

# In[ ]:

# 获取前x个交易日日期
def load_trade_date(today, before_count):
    dates = DataAPI.TradeCalGet(exchangeCD=u"XSHG,XSHE",beginDate=u"20100101",endDate=today)
    open_date = dates[dates.isOpen == 1]
    return open_date.iloc[-1 - before_count].calendarDate

today = '2021-11-30'
yesterday = load_trade_date(today, 1)
before_yes = load_trade_date(today, 2)
b_b_yes = load_trade_date(today, 3)

def load_all_tickers(today):
    # 获取某日市场股票sec_ID列表
    universe = DynamicUniverse('A')
    all_tickers = universe.preview(today, skip_halted=True)
    return all_tickers

# 滤出创业板标
def load_30(day):
    def load_30_handle(tickers):
        return tickers.startswith('30')

    tickers_30 = filter(load_30_handle, load_all_tickers(day))
    return tickers_30

import pandas as pd
pd.set_option('max_columns',1000)
pd.set_option('max_row',300)
pd.set_option('display.float_format', lambda x:' %.5f' % x)

# 拿到涨停票
def get_limit_block_data(day):
    tickers_30 = load_30(day)

    day_data = DataAPI.MktEqudGet(secID=tickers_30, tradeDate=day, field=['ticker','closePrice','chgPct','highestPrice'], pandas="1")
    up_limit_data = DataAPI.MktLimitGet(secID=tickers_30, tradeDate=day, field=['ticker','limitUpPrice'], pandas="1")
    day_data = pd.merge(day_data, up_limit_data)

    stocks_blocked = day_data[day_data.closePrice == day_data.limitUpPrice].sort_values(by='chgPct', ascending=False)
    return stocks_blocked.ticker.tolist()

# 拿到触涨停票
def get_touching_limit_block_data(day):
    tickers_30 = load_30(day)

    day_data = DataAPI.MktEqudGet(secID=tickers_30, tradeDate=day, field=['ticker','closePrice','chgPct','highestPrice'], pandas="1")
    up_limit_data = DataAPI.MktLimitGet(secID=tickers_30, tradeDate=day, field=['ticker','limitUpPrice'], pandas="1")
    day_data = pd.merge(day_data, up_limit_data)

    stocks_blocked = day_data[day_data.highestPrice == day_data.limitUpPrice].sort_values(by='chgPct', ascending=False)
    return stocks_blocked.ticker.tolist()

# 拿到1B票
def get_1B_ticker(date):
    date_before = load_trade_date(date, 1)
    now_list = get_limit_block_data(date)
    before_list = get_limit_block_data(date_before)

    return [ticker for ticker in now_list if ticker not in before_list]

# 拿到触及2B票
def get_touched_2B_ticker(date):
    date_before = load_trade_date(date, 1)
    # 当日触板票
    now_list = get_touching_limit_block_data(date)
    # 昨日1板票
    yes_1B_list = get_1B_ticker(date_before)

    return [ticker for ticker in now_list if ticker in yes_1B_list]

    # get_2B_ticker('2021-11-30') # ['300165', '300412'] 天瑞仪器、迦南科技




def get_result(date_today, date_yes):
    '''
    总逻辑
    拼装成需要的一个df返回
    '''

    yes_touched_2B_ticker = get_touched_2B_ticker(date_yes)
    print(yes_touched_2B_ticker)
    if len(yes_touched_2B_ticker) == 0:
        return

    today_info = DataAPI.MktEqudGet(ticker=yes_touched_2B_ticker, tradeDate=date_today, field=['ticker','secShortName',
                                                                      'openPrice',
                                                                      'closePrice',
                                                                      'highestPrice',
                                                                      'lowestPrice',
                                                                     ], pandas="1")

    yes_info = DataAPI.MktEqudGet(ticker=yes_touched_2B_ticker, tradeDate=date_yes, field=['secShortName',
                                                                      'closePrice',
                                                                      'highestPrice',
                                                                      'tradeDate'
                                                                     ], pandas="1").rename(columns={'closePrice':'yes_C',
                                                                                                    'highestPrice':'yes_H'
                                                                                                   })

    yes_info['昨日是否封板'] = yes_info.yes_C == yes_info.yes_H
    yes_info['昨日炸板日面'] = (yes_info.yes_C - yes_info.yes_H) / yes_info.yes_H

    final_info = pd.merge(today_info, yes_info, on='secShortName')
    final_info['溢价_O'] = (final_info.openPrice - final_info.yes_H) / final_info.yes_H
    final_info['溢价_H'] = (final_info.highestPrice - final_info.yes_H) / final_info.yes_H
    final_info['溢价_L'] = (final_info.lowestPrice - final_info.yes_H) / final_info.yes_H
    final_info['溢价_C'] = (final_info.closePrice - final_info.yes_H) / final_info.yes_H

    return final_info

# datas = pd.DataFrame(columns=['secShortName','openPrice','closePrice','highestPrice','lowestPrice','yes_C','yes_H','tradeDate','昨日是否封板','昨日炸板日面','溢价_O','溢价_H','溢价_L','溢价_C'])

# daily_data = get_result(date_today='2021-11-30', date_yes='2021-11-29')
# datas = pd.concat([datas, daily_data])

# datas
# ['300165', '300412'] 天瑞仪器、迦南科技


# In[ ]:

datas = pd.DataFrame(columns=['secShortName','openPrice','closePrice','highestPrice','lowestPrice','yes_C','yes_H','tradeDate','昨日是否封板','昨日炸板日面','溢价_O','溢价_H','溢价_L','溢价_C'])

today = '2021-11-30'
dates = DataAPI.TradeCalGet(exchangeCD=u"XSHG",beginDate=u"20210801",endDate=today)
open_date = dates[dates.isOpen == 1]

for index, row in open_date.iterrows():
    print(row.calendarDate)
    # print row.prevTradeDate
    daily_data = get_result(date_today=row.calendarDate, date_yes=row.prevTradeDate)
    # print daily_data
    datas = pd.concat([datas, daily_data])

datas = datas.reset_index(drop=True)
datas


# In[ ]:

DataAPI.MktEqudGet(ticker="301060", tradeDate='20211126', pandas="1")


# In[ ]:

# 获取涨停相关数据
# DataAPI.MktLimitGet('002374',tradeDate='20211201',field=u"secID,upLimitReachedTimes,limitUpPrice",pandas="1")
DataAPI.MktLimitGet(ticker=u"002374",tradeDate='20211201', pandas="1")
# DataAPI.MktLimitGet(ticker=u"002374",tradeDate='20211201',exchangeCD=u"",beginDate=u"",endDate=u"",field=u"",pandas="1")


# In[ ]:

# 参考了个GitNote里面的写法
# 不过没权限调用那个接口
# 我们用别的方法咯，甚至通过GET调用别的接口都行的吧

# 常量准备
import pandas as pd
from datetime import datetime as dt
from pandas import DataFrame, Series
today = dt.today().strftime('%Y%m%d')   # 获得今天的日期

# DataAPI取所有A股
stocks = DataAPI.EquGet(equTypeCD='A',listStatusCD='L',field='secID,nonrestfloatA',pandas="1")
universe = stocks['secID'].tolist()    # 转变为list格式，以便和DataAPI中的格式符合

# 取所有A股的最新行情
fields = ['shortNM','lastPrice','bidBook','askBook','suspension']
data = DataFrame()
for i in range(0,len(universe),300):   # 原则上可以性取完的，但是试验中作者发现会报错，估计是运算量太大，所以这里分批次取，每次300个
    t = DataAPI.MktTickRTSnapshotGet(securityID=universe[i:min(i+300,len(universe))],field=fields,pandas="1")
    tmp = DataFrame()
    tmp['secID'] = t['ticker']+'.'+t['exchangeCD']
    tmp[['shortNM','lastPrice','bidBook_price1','bidBook_volume1','askBook_volume1','suspension']] =t[['shortNM','lastPrice','bidBook_price1','bidBook_volume1','askBook_volume1','suspension']]
    data = pd.concat([data,tmp],axis=0)   # 数据拼接

# 去掉当日停牌的股票 
data['nonrestfloatA'] = stocks['nonrestfloatA']
data = data[data['suspension']==0]

# 去掉没有涨停板的股票
data['suspension'][(data['bidBook_volume1']>0).values & (data['askBook_volume1']==0).values] = 1  # 若涨停盘，suspension则赋值1
data = data[data['suspension']==1]
data.drop(['suspension','askBook_volume1'],axis=1,inplace=True)

# 计算封停板资金量、流通市值、两者比值
data['stop_money'] = data['bidBook_price1'].values * data['bidBook_volume1'].values
data['float_value'] = data['bidBook_price1'].values * data['nonrestfloatA'].values
data['rate'] = data['stop_money']/data['float_value']*100   #百分之几
data = data.sort(columns='rate',ascending=False).reset_index()
data.drop('index',axis=1,inplace=True)

# 重命名
data.columns = ['代码','简称','最新成交价','买一价','买一量','非受限流通股','封停板资金','流通市值','封停资金流通市值比（百分之几）']
data.head(30)


# In[ ]:

import pandas as pd

start = '20211122'                       # 回测起始时间
end = '20211130'                         # 回测结束时间
universe = DynamicUniverse('A')        # 证券池，支持股票、基金、期货、指数四种资产
freq = 'm'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测

wanted_datas = pd.DataFrame(columns=['secShortName','openPrice','closePrice','highestPrice','lowestPrice','yes_C','yes_H','tradeDate','昨日是否封板','昨日炸板日面','溢价_O','溢价_H','溢价_L','溢价_C'])
daily_datas = []

def initialize(context):

    pass

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context):
    previous_date = context.previous_date.strftime('%Y-%m-%d')
    current_date = context.now.strftime('%Y-%m-%d')
    context
#     daily_data = get_result(previous_date, previous_date)
#     daily_datas.append(daily_data)

#     wanted_datas = pd.concat([wanted_datas, daily_data])


def post_trading_day(context):
    print('今天是：')
    print(context.now)
    # if len(datas) % 20 != 2333:
        # print pd.DataFrame(datas)


# In[ ]:



