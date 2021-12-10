import TacticalCenter.Financial.common.define as define


def boom_to_block_info(stock: define.Stock, day_count: int):

    from datetime import datetime
    from datetime import timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    print(end_date)
    print(start_date)
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    bars = stock.get_bar(start_date_str, end_date_str)
    block_bars = bars[bars['pct_chg'] > 5]

    return block_bars


if __name__ == '__main__':
    # 某支股票近N天涨停数
    block_info = boom_to_block_info(stock=define.xunfei, day_count=100)
    print(block_info)
    print('涨停啦~')
