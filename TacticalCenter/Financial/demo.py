import pandas as pd
import TacticalCenter.Financial.common.define as define
import TacticalCenter.Financial.api as api
import datetime
import tushare as ts
import os


def demo_func():
    # 期望问句：
    # 20211104连板，非ST，非新股, 20211105首次涨停时间, 20211108开盘涨幅, 20211108收盘涨幅
    # 但，如此问，不会返回20211105触板但没涨停票的信息
    #
    # 故只能分两步查询：
    # 1. 20211104连板，非ST，非新股, 20211105首次涨停时间
    # 2. 1中标的20211108开盘涨幅, 20211108收盘涨幅（调TuShare接口可能比较方便？）

    bf_yes_day = '20211104'
    yes_day = '20211105'
    today = '20211108'
    five_day_later = '20211112'

    question = '{bf_yes_day}连板，非ST，非新股, ' \
               '{yes_day}首次涨停时间, {yes_day}涨幅，{yes_day}开盘涨幅'.format(bf_yes_day=bf_yes_day, yes_day=yes_day)
    print(question)

    # step 1: 拿到交易日数据 & 前一日数据
    df = api.WenCai().query_with(question)
    wanted_df = df[['股票代码',
                    '股票简称',
                    '首次涨停时间[%s]' % yes_day,
                    '涨跌幅:前复权[%s]' % yes_day,
                    '分时涨跌幅:前复权[%s 09:25]' % yes_day,
                    '连续涨停天数[%s]' % bf_yes_day,
                    '涨停封单量[%s]' % yes_day
                    ]]
    wanted_df.rename(columns={
        '首次涨停时间[%s]' % yes_day: '昨首停',
        '涨跌幅:前复权[%s]' % yes_day: '昨收',
        '分时涨跌幅:前复权[%s 09:25]' % yes_day: '昨开',
        '连续涨停天数[%s]' % bf_yes_day: '前连板',
        '涨停封单量[%s]' % yes_day: '昨封单'
    }, inplace=True)
    wanted_df['交易日(昨)'] = yes_day
    wanted_df['昨首停'] = pd.to_datetime(yes_day + wanted_df['昨首停'], format='%Y%m%d %H:%M:%S')
    print(wanted_df)

    # step 2: 找到非竞价一字 & 涨停时间最早的票
    wanted_df = wanted_df.sort_values(by='昨首停').reset_index()
    del wanted_df['index']
    print(wanted_df)

    # - - datetime处理参考：https://blog.csdn.net/phoenix339/article/details/97620818 - -
    wanted_df['昨竞一'] = wanted_df['昨首停'].dt.time == datetime.datetime.strptime('09:30:00', '%H:%M:%S').time()

    wanted_df['selected'] = False
    selected_stock = wanted_df[wanted_df.昨竞一 == False].iloc[0]
    wanted_df.loc[selected_stock.name, 'selected'] = True

    # 转为百分比
    wanted_df['昨开'] = pd.to_numeric(wanted_df['昨开']) / 100
    wanted_df['昨开'] = wanted_df['昨开'].apply(lambda x: format(x, '.2%'))
    wanted_df['昨收'] = pd.to_numeric(wanted_df['昨收']) / 100
    wanted_df['昨收'] = wanted_df['昨收'].apply(lambda x: format(x, '.2%'))
    print(wanted_df)

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
    bars: pd.DataFrame = pro.daily(ts_code=ts_code, start_date=today,
                     end_date=five_day_later)
    bars.set_index('ts_code', inplace=True)

    # 接下来，需要把值插入到如上表中了
    # ts_code作为key，然后：
    # 20211112_pct_chg: -9.8 | 20211111_pct_chg: 16.06 | 20211110_pct_chg: -0.2 | 20211109_pct_chg: 0.2 |
    # 20211108_pct_chg: x.x | 20211108_o_pct_chg: x.x
    # 1_o_pct_chg | 1_c_pct_chg | 2_c_pct_chg | 3_c_pct_chg | 4_c_pct_chg | 5_c_pct_chg

    # 做成这样的表格 

    print(bars)


if __name__ == '__main__':
    demo_func()
