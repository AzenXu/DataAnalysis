import pandas as pd
import numpy as np
import TacticalCenter.Financial.common.define as define
import TacticalCenter.Financial.api as api
import datetime
import tushare as ts
import os


def trade_days(start_date='20180101', duration=10) -> list:
    from datetime import datetime
    # 构建
    now = datetime.now().strftime('%Y%m%d')
    pro = ts.pro_api()
    df = pro.query('trade_cal', start_date=start_date, end_date=now)
    wanted_days = df[df.is_open == 1][0:duration].cal_date.to_list()
    return wanted_days


def trade_days_from_to(from_day='20211101', to_day='20211208') -> list:
    pro = ts.pro_api()
    df = pro.query('trade_cal', start_date=from_day, end_date=to_day)
    wanted_days = df[df.is_open == 1].cal_date.to_list()
    return wanted_days


def pickup_one_day_stocks(bf_trade_day='20211101') -> pd.DataFrame:
    # 期望问句：
    # 20211104连板，非ST，非新股, 20211105首次涨停时间, 20211108开盘涨幅, 20211108收盘涨幅
    # 但，如此问，不会返回20211105触板但没涨停票的信息
    #
    # 故只能分两步查询：
    # 1. 20211104连板，非ST，非新股, 20211105首次涨停时间
    # 2. 1中标的20211108开盘涨幅, 20211108收盘涨幅（调TuShare接口可能比较方便？）

    bf_yes_day = bf_trade_day
    bf_yes_day, trade_day, hold_day, day_2, day_3, day_4, day_5 = trade_days(start_date=bf_yes_day,
                                                                             duration=7)  # unpacking语句

    question = '{bf_yes_day}连板，非ST，非新股, ' \
               '{yes_day}首次涨停时间, {yes_day}涨幅，{yes_day}开盘涨幅'.format(bf_yes_day=bf_yes_day, yes_day=trade_day)

    # step 1: 拿到交易日数据 & 前一日数据
    df = api.WenCai().query_with(question)

    # bugfix: 20210208 ['分时涨跌幅:前复权[20210209 09:25]'] not in index
    # question: 20210208连板，非ST，非新股, 20210209首次涨停时间, 20210209涨幅，20210209开盘涨幅
    # 同花顺里看了下，这个字段确实没返回

    wanted_df = df[['股票代码',
                    '股票简称',
                    '首次涨停时间[%s]' % trade_day,
                    '涨跌幅:前复权[%s]' % trade_day,
                    # '分时涨跌幅:前复权[%s 09:25]' % trade_day,
                    '连续涨停天数[%s]' % bf_yes_day,
                    '涨停封单量[%s]' % trade_day
                    ]]

    if '分时涨跌幅:前复权[%s 09:25]' % trade_day in df:
        wanted_df['分时涨跌幅:前复权[%s 09:25]' % trade_day] = df['分时涨跌幅:前复权[%s 09:25]' % trade_day]
    else:
        wanted_df['分时涨跌幅:前复权[%s 09:25]' % trade_day] = np.nan

    wanted_df.rename(columns={
        '首次涨停时间[%s]' % trade_day: '昨首停',
        '涨跌幅:前复权[%s]' % trade_day: '昨收',
        '分时涨跌幅:前复权[%s 09:25]' % trade_day: '昨开',
        '连续涨停天数[%s]' % bf_yes_day: '前连板',
        '涨停封单量[%s]' % trade_day: '昨封单'
    }, inplace=True)
    wanted_df['交易日'] = trade_day
    wanted_df['昨首停'] = pd.to_datetime(trade_day + wanted_df['昨首停'], format='%Y%m%d %H:%M:%S')
    print(wanted_df)

    # step 2: 找到非竞价一字 & 涨停时间最早的票
    wanted_df = wanted_df.sort_values(by='昨首停').reset_index()
    del wanted_df['index']
    print(wanted_df)

    # - - datetime处理参考：https://blog.csdn.net/phoenix339/article/details/97620818 - -
    wanted_df['昨竞一'] = wanted_df['昨首停'].dt.time == datetime.datetime.strptime('09:30:00', '%H:%M:%S').time()

    wanted_df['selected'] = False
    # bugfix: 20210311: IndexError("single positional indexer is out-of-bounds")
    if wanted_df[wanted_df.昨竞一 == False].shape[0] > 0: # 有值，再改
        selected_stock = wanted_df[wanted_df.昨竞一 == False].iloc[0]
        wanted_df.loc[selected_stock.name, 'selected'] = True

    # # 转为百分比
    # wanted_df['昨开'] = pd.to_numeric(wanted_df['昨开']) / 100
    # wanted_df['昨开'] = wanted_df['昨开'].apply(lambda x: format(x, '.2%'))
    # wanted_df['昨收'] = pd.to_numeric(wanted_df['昨收']) / 100
    # wanted_df['昨收'] = wanted_df['昨收'].apply(lambda x: format(x, '.2%'))
    # print(wanted_df)

    # step 3: 拿到这些票"今"开涨、收涨，以及此后5日收涨
    """
    获取行情数据
    :param start_date
    :param end_date
    :return: https://tushare.pro/document/2?doc_id=27
    """
    ts.set_token(os.getenv('TUSHARE_TOKEN'))

    codes = wanted_df.股票代码.tolist()
    ts_code = ','.join(codes)
    print(ts_code)

    pro = ts.pro_api()
    bars: pd.DataFrame = pro.daily(ts_code=ts_code, start_date=hold_day,
                                   end_date=day_5)
    bars.set_index(['ts_code', 'trade_date'], inplace=True)

    # 接下来，需要把值插入到如上表中了
    # ts_code作为key，然后：
    # 20211112_pct_chg: -9.8 | 20211111_pct_chg: 16.06 | 20211110_pct_chg: -0.2 | 20211109_pct_chg: 0.2 |
    # 20211108_pct_chg: x.x | 20211108_o_pct_chg: x.x
    # 1_o_pct_chg | 1_c_pct_chg | 2_c_pct_chg | 3_c_pct_chg | 4_c_pct_chg | 5_c_pct_chg

    # 做成这样的表格

    wanted_bar: pd.DataFrame = bars['pct_chg'].unstack()
    '''
        trade_date  20211108  20211109  20211110  20211111  20211112
    ts_code                                                     
    002096.SZ    10.0213   10.0129    9.9824    9.9840  -10.0000
    002751.SZ     9.9916  -10.0038   10.0085   -5.0329   -3.8320
    002870.SZ    -1.2402   -2.3488    1.5718   -2.9308   10.0000
    003043.SZ     1.6782   -2.3951   10.0064    3.7564    2.5398
    300264.SZ     5.9957    0.2020   -0.2016   16.0606   -9.8346
    601218.SH    -7.2682    0.0000    2.0270   -1.8543    5.1282
    605555.SH    -3.0479    1.5119    1.5603   -5.4935   10.0000
    '''
    wanted_bar.rename(columns={hold_day: '1_c_chg',
                               day_2: '2_c_chg',
                               day_3: '3_c_chg',
                               day_4: '4_c_chg',
                               day_5: '5_c_chg'
                               }, inplace=True)

    wanted_df.set_index('股票代码', inplace=True)
    result_df = pd.concat((wanted_df, wanted_bar), axis=1)

    '''
                   股票简称                 昨首停           昨收  ...  3_c_chg  4_c_chg  5_c_chg
    002096.SZ  南岭民爆 2021-11-05 09:30:00  10.00781861  ...   9.9824   9.9840 -10.0000
    002751.SZ  易尚展示 2021-11-05 09:30:00  10.01855288  ...  10.0085  -5.0329  -3.8320
    605555.SH  德昌股份 2021-11-05 09:36:16  10.00767853  ...   1.5603  -5.4935  10.0000
    002870.SZ  香山股份 2021-11-05 10:13:48  10.00505306  ...   1.5718  -2.9308  10.0000
    300264.SZ  佳创视讯 2021-11-05 10:21:18  20.05141388  ...  -0.2016  16.0606  -9.8346
    601218.SH  吉鑫科技 2021-11-05 10:35:50   2.43902439  ...   2.0270  -1.8543   5.1282
    003043.SZ  华亚智能 2021-11-05 13:13:13   2.84194134  ...  10.0064   3.7564   2.5398
    '''
    return result_df


def pickup_stocks(from_day='20211207', to_day='20211208') -> pd.DataFrame:
    import time
    trade_day_list = trade_days_from_to(from_day=from_day, to_day=to_day)
    total_stocks = pd.DataFrame()
    for i, trade_day in enumerate(trade_day_list):
        one_day_stocks = pickup_one_day_stocks(trade_day)
        total_stocks = pd.concat([total_stocks, one_day_stocks])
        time.sleep(3.5)

    return total_stocks


if __name__ == '__main__':
    ts.set_token(os.getenv('TUSHARE_TOKEN'))

    # trade_days()
    result = pickup_stocks(from_day='20210201', to_day='20210401')
    result.to_csv('./strong_data_202102-03.csv')
    print(result)
