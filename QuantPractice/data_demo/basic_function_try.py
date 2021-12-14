def plot_try():
    import akshare as ak
    import mplfinance as mpf  # Please install mplfinance as follows: pip install mplfinance

    stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
    stock_us_daily_df = stock_us_daily_df[["open", "high", "low", "close", "volume"]]
    stock_us_daily_df.columns = ["Open", "High", "Low", "Close", "Volume"]
    stock_us_daily_df.index.name = "Date"
    stock_us_daily_df = stock_us_daily_df["2021-04-01": "2021-12-10"]
    mpf.plot(stock_us_daily_df, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=False)


def zt_pool():
    import akshare as ak
    # stock_em_zt_pool_df = ak.stock_em_zt_pool(date='20211210')
    # print(stock_em_zt_pool_df)


def minute_load():
    import akshare as ak
    # # 东财
    # stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001", period='1', adjust='',
    #                                                       start_date="2021-12-06 09:32:00",
    #                                                       end_date="2021-12-10 09:32:00")
    # print(stock_zh_a_hist_min_em_df)

    # 渣浪
    stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
    print(stock_zh_a_minute_df)


def tick_load():
    import akshare as ak

    stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(code="sh600848", trade_date="20191011")
    print(stock_zh_a_tick_tx_df)


if __name__ == '__main__':
    # zt_pool()
    # minute_load()
    tick_load()
    pass
