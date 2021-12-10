import sqlite3

'''
    '000001': 
    {'name': '上证指数', 
    'open': 3376.4402, 
    'close': 3367.9658, 
    'now': 3371.0011, 
    'high': 3390.5593, 
    'low': 3352.5017, 
    'buy': 0.0, 
    'sell': 0.0, 
    'turnover': 269562222, 
    'volume': 377507238826.0, 
    'bid1_volume': 0, 'bid1': 0.0, 
    'bid2_volume': 0, 'bid2': 0.0, 
    'bid3_volume': 0, 'bid3': 0.0, 
    'bid4_volume': 0, 'bid4': 0.0, 
    'bid5_volume': 0, 'bid5': 0.0, 
    'ask1_volume': 0, 'ask1': 0.0, 
    'ask2_volume': 0, 'ask2': 0.0, 
    'ask3_volume': 0, 'ask3': 0.0, 
    'ask4_volume': 0, 'ask4': 0.0, 
    'ask5_volume': 0, 'ask5': 0.0, 
    'date': '2020-08-04', 
    'time': '11:35:03'}
'''


def data_store(data_dic):
    conn = sqlite3.connect('../../../Stock.sqlite')
    cursor = conn.cursor()

    cursor.execute('insert into stock_tick (stock_id, timest) values (\'800001\', 888888)')

    cursor.close()
    conn.commit()
    conn.close()


def data_read():
    conn = sqlite3.connect('../../../Stock.sqlite')
    cursor = conn.cursor()
    cursor.execute('select * from stock_tick')
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    data_store({})

    data_read()
