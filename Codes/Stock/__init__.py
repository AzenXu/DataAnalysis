import tushare as ts
import os
import Stock.first_exmaple as first_example

def init():
    ts.set_token(os.getenv('TUSHARE_TOKEN'))

if __name__ == '__main__':
    init()
    first_example.main()
else:
    print('package init successful')






