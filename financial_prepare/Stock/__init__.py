import tushare as ts
import os
import financial_prepare.Stock.first_exmaple as first_example
import financial_prepare.Stock.second_example as second_example


def init():
    ts.set_token(os.getenv('TUSHARE_TOKEN'))


if __name__ == '__main__':
    init()
    # first_example.main()
    second_example.main()
else:
    print('package init successful')
