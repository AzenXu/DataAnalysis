from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams

if __name__ == '__main__':
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        # data = api.to_df(api.get_security_bars(9, 0, '000001', 0, 10))
        data = api.to_df(api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 1000, 2000, 20210209))
        print(data)
