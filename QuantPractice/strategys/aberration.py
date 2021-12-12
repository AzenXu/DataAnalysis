import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tushare as ts
import os
import QuantPractice.strategys.define as define

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

observer_length = 10
open_n = 0.5
stop_win_n = 3
stop_lose_static_n = 1
stop_lose_dynamic_n = 0

# stock = define.xunfei
stock = define.mengjie

if __name__ == '__main__':
    ts.set_token(os.getenv('TUSHARE_TOKEN'))
    # 拿数据
    # pro = ts.pro_api()
    df: pd.DataFrame = ts.pro_bar(ts_code=define.xunfei.code,
                                  asset=define.xunfei.asset,
                                  start_date='20210101',
                                  end_date='20211201',
                                  adj='qfq')
    # df: pd.DataFrame = ts.pro_bar(ts_code=define.xunfei.code,
    #                               asset=define.xunfei.asset,
    #                               start_date='201900101',
    #                               end_date='20200601',
    #                               adj='qfq')
    # df: pd.DataFrame = ts.pro_bar(ts_code=stock.code,
    #                               asset=stock.asset,
    #                               start_date='20120101',
    #                               end_date='20130620',
    #                               adj='qfq')  # 1
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    # df.set_index('trade_date', inplace=True)
    df.sort_values('trade_date', inplace=True)
    df.reset_index(inplace=True)
    del df['index']

    df['ma'] = df.close.rolling(window=observer_length, min_periods=3).mean()
    df['last_ma'] = df.ma.shift()
    df['last_close'] = df.close.shift()
    df['std'] = df.close.rolling(window=observer_length, min_periods=3).std()
    df['std_rolling_max'] = df['std'].rolling(window=observer_length).max()
    df['last_std_rolling_max'] = df['std_rolling_max'].shift()

    # 上策略
    df['open_long_price'] = df.last_ma + open_n * df.last_std_rolling_max
    df['stop_win_price'] = df.last_ma + stop_win_n * df.last_std_rolling_max
    df['stop_lose_dynamic'] = df.last_ma - stop_lose_dynamic_n * df.last_std_rolling_max

    # 开仓信号：涨超开仓价 & 开仓价 > 动态止损价
    # df['open_signal'] = np.where((df.high > df.open_long_price) & (df.open_long_price > df.stop_lose_dynamic), 1, 0)
    df['open_signal'] = np.where((df.high > df.open_long_price), 1, 0)
    df['stop_win_signal'] = np.where(df.high > df.stop_win_price, 1, 0)

    df = df.dropna()
    df['return'] = np.nan
    df.reset_index(inplace=True)
    del df['index']

    position = 0
    stop_lose_price_static = float('inf')
    # (次日)需要按开盘价卖出
    need_sell_as_open = False
    for i in range(len(df)):
        stock_daily = df.iloc[i]
        if position == 0 and stock_daily['open_signal'] == 1:
            # 开仓
            position = 1
            # 算当日return
            open_long_price = max(stock_daily['open'], stock_daily['open_long_price'])
            df.loc[i, 'return'] = stock_daily['close'] / open_long_price - 1
            # 算止损价
            stop_lose_price_static = open_long_price - stop_lose_static_n * stock_daily['last_std_rolling_max']
            # 若开仓当日满足平仓条件，则标记之
            need_sell_as_open = (
                    stock_daily['low'] < max(stop_lose_price_static, stock_daily['stop_lose_dynamic'])
                    or stock_daily['stop_win_signal']
            )

        elif position == 1:
            stop_lose_price_daily = max(stop_lose_price_static, stock_daily['stop_lose_dynamic'])
            need_stop_lose = stock_daily['low'] < stop_lose_price_daily
            need_stop_win = stock_daily['stop_win_signal'] == 1
            # 判断开盘平仓
            if need_sell_as_open:
                # 平仓
                position = 0
                # 算收益 - 今开 / 昨收
                df.loc[i, 'return'] = stock_daily['open'] / stock_daily['last_close'] - 1
                # 更新标记
                need_sell_as_open = False
            elif need_stop_lose:
                # 平仓
                position = 0
                # 算收益
                sell_price = min(stock_daily['open'], stop_lose_price_daily)
                df.loc[i, 'return'] = sell_price / stock_daily['last_close'] - 1
            elif need_stop_win:
                position = 0
                df.loc[i, 'return'] = stock_daily['stop_win_price'] / stock_daily['last_close'] - 1
            else:
                # 算持仓收益
                df.loc[i, 'return'] = stock_daily['close'] / stock_daily['last_close'] - 1

    # 算收益
    df['return'].fillna(0, inplace=True)
    df['strategy_return'] = (df['return'] + 1).cumprod()
    df['stock_return'] = (df['close'].pct_change() + 1).cumprod()

    df.set_index('trade_date', inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df.stock_return)
    ax.plot(df.strategy_return)
    plt.title(stock.name)
    plt.show()

    print('go go go ~')
