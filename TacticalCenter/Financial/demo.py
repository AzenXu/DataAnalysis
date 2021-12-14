import pandas as pd
import TacticalCenter.Financial.common.define as define
import TacticalCenter.Financial.api as api
import datetime


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

    question = '{bf_yes_day}连板，非ST，非新股, ' \
               '{yes_day}首次涨停时间, {yes_day}涨幅，{yes_day}开盘涨幅'.format(bf_yes_day=bf_yes_day, yes_day=yes_day)
    print(question)

    # step 1: 拿到交易日数据 & 前一日数据
    df = api.WenCai().query_with(question)
    wanted_df = df[['code',
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
    no_start_from_limited = wanted_df[
        wanted_df['昨首停'].dt.time > datetime.datetime.strptime('09:30:00', '%H:%M:%S').time()]
    print(no_start_from_limited.iloc[0])

    # step 3: 拿到这支票"今天"开盘涨幅、收盘涨幅。
    # - 如果收盘涨停，则继续取下一日，直到收盘非涨停
    # - 如果收盘跌停，则继续取下一日，直到收盘非跌停



if __name__ == '__main__':
    demo_func()
