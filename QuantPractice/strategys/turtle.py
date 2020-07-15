# 加载库函数
import numpy as np
import pandas as pd
import talib as ta  # 加载技术分析库
from talib.abstract import *

# 初始化回测环境
start = '20150201'  # 回测起始时间 注：支持两种日期表述形式（ '2015-01-01'，'20150101'）
end = '20150601'  # 回测结束时间
benchmark = 'SH50'  # 策略参考标准为上证50指数
universe = set_universe('SH50')  # 选股范围为上证50成分股
freq = 'd'  # 用日线回测的策略
refresh_rate = 1  # 每1日调一次仓，即每个交易日都会运行第三部分的handle_data函数

# 初始化投资者（账户）参数
# accounts为字典类型，代表投资者所有的账户，而字典中每一个键代表一个账户，而每一个键对应的值为该账户的初始情况，如本程序中的键为fantasy_account（股票账户），值为相应配置
accounts = {
    'fantasy_account': AccountConfig(account_type='security', capital_base=10000000)  # 初始化投资者的股票账户： 投资品种为股票，初始投资金额为1千万
}

# 初始化策略参数:
Max_Position_per = 0.1  # 每只股票购入的最高比例为10%
max_history_window = 250  # 设置最长回测周期
Max_time_range = 60  # 设置数据回顾周期
limit_unit = 4  # 限制最多买入的单元数
atrlength = 20  # 计算真实波幅考虑的周期数
DC_range = 20  # 计算DC通道考虑的周期数
trade_percent = 0.01  # 每次交易占总资产比例的基础值

record = pd.DataFrame({
    'symbol': [],
    'add_time': [],
    'last_buy_price': []
})  # 股票及对应的加仓次数和上一次买价


def calcUnit(portfolio_value, ATR):
    '''
     计算unit,注意股数为100的整数倍
    '''
    value = portfolio_value * trade_percent
    return int((value / ATR) / 100) * 100


def timing_turtle(context):
    global record
    # 数据获取（通用部分）：投资者账户，可供投资股票，价格数据，持仓数据，账户金额数据
    account = context.get_account('fantasy_account')
    current_universe = context.get_universe(asset_type='stock', exclude_halt=True)
    history = context.history(current_universe, ['closePrice', 'lowPrice', 'highPrice'], Max_time_range, rtype='array')
    security_position = account.get_positions()
    cash = account.cash

    for sec in current_universe:
        close = history[sec]['closePrice']  # 获取股票sec过去Max_time_range天的收盘价
        low = history[sec]['lowPrice']  # 获取股票sec过去Max_time_range天的最低价
        high = history[sec]['highPrice']  # 获取股票sec过去Max_time_range天的最高价
        current_price = context.current_price(sec)  # 获得当前时刻价格

        # 计算ATR
        atr = ta.ATR(high, low, close, atrlength)[-1]
        # 计算上下轨
        upper_tunnel = high[-DC_range:-1].max()
        lower_tunnel = low[-int(DC_range / 2):-1].min()

        # 「建仓策略」：突破DC通道上轨
        if current_price > upper_tunnel and sec not in security_position:
            # 买入
            account.order_to(sec, calcUnit(account.portfolio_value, atr))
            # 清记录
            if len(record) != 0:
                record = record[record['symbol'] != sec]
            # 加记录
            record = record.append(
                pd.DataFrame({
                    'symbol': [sec],
                    'add_time': [1],
                    'last_buy_price': [current_price]
                })
            )
        # 有持仓
        elif sec in security_position:
            # 上次买入价
            last_price = float(record[record['symbol'] == sec]['last_buy_price'])
            # 可加仓价格
            add_price = last_price + 0.5 * atr
            # 已加仓次数
            added_times = float(record[record['symbol'] == sec]['add_time'])

            # 「加仓策略」：价格上涨超过0.5N并且加仓次数小于4次
            if current_price > add_price and added_times < limit_unit:
                # 下单
                account.order(sec, calcUnit(account.portfolio_value, atr))
                # 改记录
                record.loc[record['symbol'] == sec, 'add_time'] = record[record['symbol'] == sec]['add_time'] + 1
                record.loc[record['symbol'] == sec, 'last_buy_price'] = current_price
            # 「清仓策略」
            # 止损：价格相对上个买入价下跌2ATR
            # 止盈：股价跌破10日唐奇安通道
            elif current_price < lower_tunnel or current_price < (last_price - 2 * atr):
                # 清仓
                account.order_to(sec, 0)
                # 清记录
                record = record[record['symbol'] != sec]


# 初始化回测环境，指明创建账户时的工作，全局只运行一次
def initialize(context):
    pass


# handle_data函数是策略的核心函数，包含了所有策略算法的内容，包括数据获取，交易信号生成，订单委托等逻辑。
# handle_data函数无论是回测还是模拟交易场景，这个函数会根据回测频率 freq 的设置被调用。当freq='d'时，每天被调用一次，当freq='m'时，每分钟被调用一次。
def handle_data(context):
    timing_turtle(context)  # 基于海龟交易系统的择时策略