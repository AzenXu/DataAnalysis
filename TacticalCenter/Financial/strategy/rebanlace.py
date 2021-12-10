import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series
from TacticalCenter.Financial.common import define
from typing import Dict


class Strategy:
    def run(self, start_date: str, end_date: str) -> pd.Series:
        pass


class Rebalance(Strategy):
    asset_one: define.Stock
    asset_two: define.Stock
    ratio_limit: float

    portfolio_net: float

    asset_one_ratio: float
    asset_two_ratio: float

    asset_one_net: float
    asset_two_net: float

    portfolio_net_change_record: Dict

    def __init__(self,
                 asset_one: define.Stock,
                 asset_two: define.Stock,
                 ration_limit=0.55,
                 asset_one_setup_ratio=0.5,
                 asset_two_setup_ratio=0.5
                 ):
        self.asset_one = asset_one
        self.asset_two = asset_two
        self.ratio_limit = ration_limit
        self.asset_one_setup_ratio = asset_one_setup_ratio
        self.asset_two_setup_ratio = asset_two_setup_ratio

        self.portfolio_net = 1

        self.asset_one_ratio = 0.5
        self.asset_two_ratio = 0.5

        self.asset_one_net = self.portfolio_net * self.asset_one_ratio
        self.asset_two_net = self.portfolio_net * self.asset_two_ratio

        self.portfolio_net_change_record = {}
        self.rebalance_record = {}

    def daily_operate(self, daily_returns: pd.Series):
        # 更新两份净值
        self.asset_one_net *= daily_returns[self.asset_one.name] + 1
        self.asset_two_net *= daily_returns[self.asset_two.name] + 1
        # 更新总净值
        self.portfolio_net = self.asset_one_net + self.asset_two_net
        # 更新两份占比
        self.asset_one_ratio = self.asset_one_net / self.portfolio_net
        self.asset_two_ratio = self.asset_two_net / self.portfolio_net
        # 记录当日总净值
        self.portfolio_net_change_record[daily_returns.name] = self.portfolio_net

        # 调仓逻辑
        def check_and_rebalance():
            if max(self.asset_one_ratio, self.asset_two_ratio) < self.ratio_limit:
                return

            self.rebalance_record[daily_returns.name] = {self.asset_one.name: self.asset_one_ratio,
                                                         self.asset_two.name: self.asset_two_ratio}
            self.asset_one_ratio = self.asset_one_setup_ratio
            self.asset_one_net = self.portfolio_net * self.asset_one_ratio
            self.asset_two_ratio = self.asset_two_setup_ratio
            self.asset_two_net = self.portfolio_net * self.asset_two_ratio

        check_and_rebalance()

        return pd.Series({
            self.asset_one.name: self.asset_one_ratio,
            self.asset_two.name: self.asset_two_ratio
        }, name=daily_returns.name)

    def run(self, start_date: str, end_date: str) -> pd.Series:
        print('rebalance running~~~')
        asset_one_closes = self.asset_one.get_bar(start_date, end_date)['close']
        asset_two_closes = self.asset_two.get_bar(start_date, end_date)['close']

        one_return = asset_one_closes.pct_change()
        two_return = asset_two_closes.pct_change()

        assets = pd.DataFrame({
            self.asset_one.name: one_return,
            self.asset_two.name: two_return
        })
        assets.dropna(inplace=True)

        # 按日进行数据操作
        assets_net = assets.apply(self.daily_operate, axis=1)  # 1
        print(assets_net)

        return pd.Series(self.portfolio_net_change_record, name='rebalance_strategy')


class Portfolio:
    returns: Series = None
    benchmark_returns: Series = None

    def __init__(self):
        pass

    def run(self, strategy: Strategy, start, end):
        self.returns = strategy.run(start, end)
        self.benchmark_returns = define.hs300.get_cum_returns(start, end)
        self.benchmark_returns.name = 'hs300'

    def draw_strategy_return(self):
        pd.concat([self.returns, self.benchmark_returns], axis=1).plot()
        plt.show()
        pass


if __name__ == '__main__':
    portfolio = Portfolio()
    portfolio.run(strategy=Rebalance(asset_one=define.debtETF, asset_two=define.zz500ETF), start='20200620',
                  end='20200720')
    portfolio.draw_strategy_return()
    print('this is a strategy using debt and stock rebalance.')
