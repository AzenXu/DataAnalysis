from Stock.DataLoader import DataLoader
from pandas import DataFrame, Series, datetime
import matplotlib.pyplot as plt
from enum import IntEnum

def wanted_first(df: DataFrame):
    print(
    '''
    计算该股票历史数据的5日均线和30日均线
    均线：
        对于每一个交易日，都可以计算出前N天德移动平均值，然后把这些移动平均值连起来，成为一条线，就叫做N日移动平均线
        N=5 - 5日均线
        
    均值计算：
        MA = (C1+C2+C3+...+Cn)/N
            C: 某日收盘价
    '''
    )

    # df = df.head(60)

    # 自己思路：遍历...for (i = 0; i < (总数 - 4); i++) {(list[i]+list[i+1]+...list[i+4]) / 5 ... ... }
    # 实现 ---
    # rolling - 按组移动
    # mean - 求均值
    ma5 = df['close'].rolling(5).mean()
    df['ma5'] = ma5
    ma30 = df['close'].rolling(30).mean()
    df['ma30'] = ma30

    # 画线 - 5日线 & 3日线
    plt.plot(ma5, label='ma5')
    plt.plot(ma30, label='ma30')
    plt.xlabel('date')
    plt.ylabel('mean_close')
    # plt.show()

    # 找「金叉」「死叉」
    # 金叉：短期均线上穿长期均线，叫金叉
    #      上：今天ma5 < 昨天ma5
    #      穿：今天ma5 > 今天ma30 & 昨天ma5 < 昨天ma30
    # 死叉：短期均线下穿长期均线，叫死叉
    #      下：今天ma5 < 昨天ma5
    #      穿：今天ma5 < 今天ma30 & 昨天ma5 > 昨天ma30
    # 策略：金叉买入，死叉卖出
    # 自己的思路：遍历...麻油...

    df['last_ma5'] = df['ma5'].shift(1) # 用shift(1)实现了「前一日」逻辑，巧妙
    df['last_ma30'] = df['ma30'].shift(1)

    golden_cross_judgement = (df['ma5'] > df['last_ma5'])\
                             & (df['ma5'] > df['ma30']) \
                             & (df['last_ma5'] < df['last_ma30'])
    death_cross_judgement = (df['ma5'] < df['last_ma5'])\
                            & (df['ma5'] < df['ma30'])\
                            & (df['last_ma5'] > df['last_ma30'])

    golden_cross_data = df.loc[golden_cross_judgement]
    death_cross_data = df.loc[death_cross_judgement]
    golden_cross_date = golden_cross_data.index
    death_cross_date = death_cross_data.index

    # 初始资金10w，金叉次日开盘全买，死叉次日开盘全卖。到今天，收益如何？
    # 若最后一次交易为金叉，只能买入，无法卖出。若有剩余股票，计算到总收益中

    # 做法：把金叉时间定义为1，死叉时间定义为0
    class Operation(IntEnum):
        BUY = 1
        SELL = 0

    s1 = Series(data=Operation.BUY, index=golden_cross_date)
    s2 = Series(data=Operation.SELL, index=death_cross_date)
    s = s1.append(s2) # 所有金叉死叉时间
    s.sort_index(inplace=True) # 排序之后，按0、1做买卖
    # 之后遍历s

    first = 100000 # 初识资金
    current_money = first # 实时资金
    hold_count = 0 # 持有的股票只数
    df['next_open'] = df['open'].shift(-1) # 要用次日开盘价买/卖
    for i in range(len(s)):
        operation = s[i]
        current_date = s.index[i]
        # current_stock = df.loc(current_date)
        current_stock = df.loc[current_date] # 被方括号还是括弧卡了一个多小时...汗了...
        price = current_stock['next_open']
        if operation == Operation.BUY:# 买
            # 算次日，买一手的花销
            hand_count = current_money // (price * 100) # 整除
            hold_count += hand_count * 100
            current_money -= hand_count * 100 * price
            print('%s: 买买买，现有%i元，持股%i只' % (current_date, current_money, hold_count))
        elif operation == Operation.SELL:
            current_money += hold_count * price
            hold_count = 0
            print('%s: 清仓清仓，现有%i元'% (current_date, current_money))
        else: # 卖
            pass

    # 特殊情况：最后一次交易是买入，用最后一日收盘价算股票账面价值
    stock_value = hold_count * df['close'][-1]

    total_benefit = stock_value + current_money


    print('Good job! Awesome baby~ 总收益是%i' % total_benefit)


def main():
    df = DataLoader.load_data('002230.sz')
    DataLoader.data_clear(df)
    # 数据按时间升序
    df = df.sort_index(ascending=True)

    wanted_first(df)

    print('done baby~')