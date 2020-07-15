# coding: utf-8

# ## Base

# In[ ]:

class Logger:
    def log(self, item):
        # log.info(item)
        pass


class SignalType:
    Open = 'SignalType.Open'
    Close = 'SignalType.Close'
    Long = 'SignalType.Long'
    Short = 'SignalType.Short'


class Checker:
    def __init__(self):
        self.logger = Logger()

    def set_signal_callback(self, signal_callback):
        self.signal_callback = signal_callback

    def test(self):
        self.signal_callback(u'哈哈哈')

    def daily_check(self, daily_context):
        pass


class Trader(object):
    def __init__(self, account_name):
        self.account_name = account_name
        self.logger = Logger()
        self.checkers = []

    def adopt_checkers(self):
        '''
        一些Trader需要有自己的checker，用来每日检查市场情况，发出「加仓」「减仓」信号
        这些checker会被过继给manager同一管理，做每日调度
        '''
        print('adopt_checkers is doing')
        return self.checkers

    def deal_with_signal(self, signal, daily_context, checker_name):
        print(u'trader is dealing with the signal:')
        print(signal)
        print('from: %s' % checker_name)


class Manager:
    def __init__(self, checkers, trader):
        self.trader = trader

        # 和trader无关checkers
        # 纯看市场（如突破BOLL带之类），发出开仓、清仓信号
        self.checkers = checkers
        # 和trader相关的checker
        # 需要基于仓位看市场，发出加仓、减仓信号
        self.adopted_checkers = self.trader.adopt_checkers()

        map(lambda x: x.set_signal_callback(self.signal_callback), self.checkers)
        map(lambda x: x.set_signal_callback(self.signal_callback), self.adopted_checkers)

    def signal_callback(self, signal, checker_name='Anonymous'):
        self.trader.deal_with_signal(signal, self.daily_context, checker_name)

    def daily(self, daily_context):
        self.daily_context = daily_context
        # 先处理有持仓的
        for adopted_checker in self.adopted_checkers:
            adopted_checker.daily_check(daily_context)

        # 后处理市场信号的
        for checker in self.checkers:
            checker.daily_check(daily_context)


# ## TraderDogs
#
# 用于替Trader嗅探某支股票的市场数据

# In[ ]:

import talib as ta


class TraderDog:
    @classmethod
    def ATR_sniff(self, sec, context, ATR_duration):
        current_universe = context.get_universe(asset_type='stock', exclude_halt=True)
        history = context.history(current_universe, ['closePrice', 'lowPrice', 'highPrice'], 60, rtype='array')

        close = history[sec]['closePrice']
        low = history[sec]['lowPrice']
        high = history[sec]['highPrice']
        # 计算ATR
        atr = ta.ATR(high, low, close, ATR_duration)[-1]

        return atr


# ## Traders

# In[ ]:

class MindlessTrader(Trader):
    '''
    开仓：信号外的股票清仓，信号内的股票买入10000
    '''

    def deal_with_signal(self, signal, daily_context, checker_name):
        # 获取当前账户信息
        account = daily_context.get_account(self.account_name)
        if signal.has_key(SignalType.Open):

            current_position = account.get_positions(exclude_halt=True)
            target_position = signal[SignalType.Open]

            # 卖出当前持有，但目标持仓没有的部分
            for stock in set(current_position).difference(target_position):
                account.order_to(stock, 0)

            # 根据目标持仓权重，逐一委托下单
            for stock in target_position:
                account.order(stock, 10000)


# In[ ]:

from copy import copy
import pandas as pd


# 不支持
# import weakref

class TurtleChecker(Checker):

    def __init__(self, trader):
        # super(TurtleChecker, self).__init__()
        self.weak_trader = trader  # weakref.ref(trader)
        print('I am turtle checker')

    def daily_check(self, daily_context):
        log.info('Trutle_Checker is working')

        previous_date = daily_context.previous_date.strftime('%Y-%m-%d')

        # # 寻找未达最大买入unit数的
        # stocks = self.weak_trader.record[self.weak_trader.record['order_count'] < self.weak_trader.max_unit_num]

        stocks_dic = self.weak_trader.record.set_index('symbol')['last_buy_price'].to_dict()
        stocks_dic_count = self.weak_trader.record.set_index('symbol')['order_count'].to_dict()
        current_universe = daily_context.get_universe(asset_type='stock', exclude_halt=True)

        long_stocks = []
        close_stocks = []

        for stock, last_price in stocks_dic.items():
            # 跳过停牌股
            if stock not in current_universe:
                continue

            ATR = TraderDog.ATR_sniff(stock, daily_context, self.weak_trader.ATR_duration)
            add_price = last_price + self.weak_trader.long_ATR_multiple * ATR
            close_price = last_price - self.weak_trader.close_ATR_multiple * ATR
            current_price = daily_context.current_price(stock)
            order_count = stocks_dic_count[stock]

            # log.warn(
            #         '\n {stock} \n 现价: {current_price} \n 止损价: {close_price} \n 最后买入价: {last_price} \n ATR: {ATR}'.format(stock=stock, current_price=current_price, close_price=close_price, last_price=last_price, ATR=ATR)
            #     )

            if current_price > add_price and order_count < 4:
                log.warn(
                    '\n {stock} need long! \n current price: {current_price} \n add price: {add_price} \n ATR: {ATR}'.format(
                        stock=stock, current_price=current_price, add_price=add_price, ATR=ATR)
                )
                long_stocks.append(stock)
            elif current_price <= close_price:
                log.warn(
                    '\n {stock} need close! \n current price: {current_price} \n close price: {close_price} \n ATR: {ATR}'.format(
                        stock=stock, current_price=current_price, close_price=close_price, ATR=ATR)
                )
                close_stocks.append(stock)

        self.signal_callback({
            SignalType.Long: long_stocks,
            SignalType.Close: close_stocks
        }, checker_name='TurtleChecker')


class TurtleTrader(Trader):

    def __init__(self, account_name,
                 risk_acceptable_percent,
                 compartment_count,
                 max_unit_num=4,
                 ATR_duration=20,
                 long_ATR_multiple=0.5,  # 加仓ATR倍数
                 close_ATR_multiple=2  # 止损ATR倍数
                 ):
        '''
        risk_acceptable_percent: 一次最大波动，所能造成的资产损失百分比
        compartment_count: 分仓数
        '''
        super(TurtleTrader, self).__init__(account_name)
        self.risk_acceptable_percent = risk_acceptable_percent
        self.compartment_count = compartment_count
        self.max_unit_num = max_unit_num
        self.ATR_duration = ATR_duration
        self.long_ATR_multiple = long_ATR_multiple
        self.close_ATR_multiple = close_ATR_multiple
        self.checkers = [TurtleChecker(self)]

        self.record = pd.DataFrame({
            'symbol': [],
            'order_count': [],
            'last_buy_price': []
        })

    def adopt_checkers(self):
        '''
        一些Trader需要有自己的checker，用来每日检查市场情况，发出「加仓」「减仓」信号
        这些checker会被过继给manager同一管理，做每日调度
        '''
        print('adopt_checkers is doing')
        return self.checkers

    def calculate_unit(self, portfolio_value, ATR):
        '''
         计算unit,注意股数为100的整数倍
        '''
        risk_acceptable_value = portfolio_value / self.compartment_count * self.risk_acceptable_percent
        # ATR：波动价/股
        # risk_acceptable_value：可承受风险总价
        stock_count = int((risk_acceptable_value / ATR) / 100) * 100

        log.warn('\n 计算unit：\n portfolio_value: %f, \n risk_acceptable_value: %f, \n ATR: %f, \n stock_count：%f' % (
            portfolio_value, risk_acceptable_value, ATR, stock_count))

        return stock_count

    def deal_with_close(self, target_position, daily_context):
        account = daily_context.get_account(self.account_name)

        close_compartments = set(self.positions.keys()).intersection(target_position)
        for stock in close_compartments:
            account.order_to(stock, 0)
            self.record = self.record[self.record['symbol'] != stock]

            log.error('\n close for {stock} \n current record is {record}'.format(stock=stock, record=self.record))

    def deal_with_open(self, target_position, daily_context):
        account = daily_context.get_account(self.account_name)

        # 分仓逻辑：仓位 - 已持仓位数 = 剩余仓位数
        compartment_vacuum = self.compartment_count - len(self.record)
        new_stocks = set(target_position).difference(self.record.symbol.values.tolist())
        new_stocks = list(new_stocks)[:compartment_vacuum]

        # 买一个Unit
        for stock in new_stocks:
            ATR = TraderDog.ATR_sniff(stock, daily_context, self.ATR_duration)
            account.order(stock, self.calculate_unit(account.portfolio_value, ATR))
            price = daily_context.current_price(stock)  # 获得当前时刻价格

            self.record = self.record.append(
                pd.DataFrame({
                    'symbol': [stock],
                    'order_count': [1],
                    'last_buy_price': [price]
                })
            )

            log.error('\n open for {stock} \n current record is {record}'.format(stock=stock, record=self.record))

    def deal_with_long(self, target_position, daily_context):
        account = daily_context.get_account(self.account_name)

        for stock in target_position:
            ATR = TraderDog.ATR_sniff(stock, daily_context, self.ATR_duration)
            account.order(stock, self.calculate_unit(account.portfolio_value, ATR))
            price = daily_context.current_price(stock)  # 获得当前时刻价格

            # 改记录
            self.record.loc[self.record['symbol'] == stock, 'last_buy_price'] = price
            self.record.loc[self.record['symbol'] == stock, 'order_count'] = self.record[self.record[
                                                                                             'symbol'] == stock].order_count + 1

            log.error('\n long for {stock} \n current record is {record}'.format(stock=stock, record=self.record))

    def deal_with_signal(self, signal, daily_context, checker_name):
        account = daily_context.get_account(self.account_name)

        # log.info('{checker_name}传来了信号：{signal}'.format(checker_name=checker_name, signal=signal))

        # 解决下单后account不实时更新问题
        self.positions = copy(account.get_positions(exclude_halt=True))

        if signal.has_key(SignalType.Close):
            self.deal_with_close(signal[SignalType.Close], daily_context)

        if signal.has_key(SignalType.Open):
            self.deal_with_open(signal[SignalType.Open], daily_context)

        if signal.has_key(SignalType.Long):
            self.deal_with_long(signal[SignalType.Long], daily_context)


# ## Checkers

# In[ ]:

class PEChecker(Checker):
    '''
    买PE前100小的公司
    '''

    def daily_check(self, daily_context):
        previous_date = daily_context.previous_date.strftime('%Y-%m-%d')
        hist = daily_context.history(symbol=daily_context.get_universe(exclude_halt=True),
                                     attribute='PE',
                                     time_range=1,
                                     style='tas')[previous_date]

        # 将因子值从小到大排序，并取前100支股票作为目标持仓
        signal = hist['PE'].order(ascending=True)
        wantted_stocks = signal[:100].index

        self.signal_callback({
            SignalType.Open: wantted_stocks
        })
        # self.signal_callback(wantted_stocks)


# In[ ]:

class DCChecker(Checker):
    '''
    唐奇安通道调查员

    上轨：前20日高
    下轨：前10日低
    建仓信号：破上轨
    平仓信号：破下轨
    '''

    DC_Range = 20

    def DC_stock_assess(self, stockID, close_history, high_history, low_history, yesterday_date):
        '''
        上轨：历史最高
        下轨：历史最低
        突破上轨，开仓；穿下轨，平仓
        '''
        close = close_history[stockID]['closePrice']
        upper_tunnel = high_history[stockID]['highPrice']
        lower_tunnel = low_history[stockID]['lowPrice']

        yesterday_price = close[-1]
        yes_upper = upper_tunnel[1:-1].max()
        yes_lower = lower_tunnel[1:-1].min()

        before_yes_price = close[-2]
        before_yes_upper = upper_tunnel[:-2].max()
        before_yes_lower = lower_tunnel[:-2].min()

        # log.info('{sec} \n current={current_price} \n upper={upper}'.format(sec=stockID, current_price=yesterday_price, upper=yes_upper))

        should_open = before_yes_price < before_yes_upper and yesterday_price > yes_upper
        should_close = before_yes_price > before_yes_lower and yesterday_price < yes_lower

        # 埋点
        if should_open:
            self.logger.log({
                'ID': stockID,
                'date': yesterday_date,
                'yes_u': yes_upper,
                'yes_p': yesterday_price,
                'yes_l': yes_lower,
                'bef_u': before_yes_upper,
                'bef_p': before_yes_price,
                'bef_l': before_yes_lower
            })
        elif should_close:
            self.logger.log({
                'ID': stockID,
                'date': yesterday_date,
                'yes_u': yes_upper,
                'yes_p': yesterday_price,
                'yes_l': yes_lower,
                'bef_u': before_yes_upper,
                'bef_p': before_yes_price,
                'bef_l': before_yes_lower
            })

        return (should_open, should_close)

    def daily_check(self, daily_context):

        log.info('DC_Checker is working')

        open_list = []
        close_list = []

        yesterday_date = daily_context.previous_date.strftime('%Y-%m-%d')
        current_universe = daily_context.get_universe(exclude_halt=True)

        close_history = daily_context.history(current_universe, 'closePrice', DCChecker.DC_Range, rtype='array')
        high_history = daily_context.history(current_universe, 'highPrice', DCChecker.DC_Range + 1, rtype='array')
        low_history = daily_context.history(current_universe, 'lowPrice', DCChecker.DC_Range / 2 + 1, rtype='array')

        for sec in current_universe:
            should_open, should_close = self.DC_stock_assess(sec, close_history, high_history, low_history,
                                                             yesterday_date)

            if should_open:
                open_list.append(sec)
            elif should_close:
                close_list.append(sec)

        self.signal_callback({
            SignalType.Open: open_list,
            SignalType.Close: close_list
        }, checker_name='DCChecker')


# ## Main

# In[ ]:

start = '2020-02-01'  # 回测起始时间
end = '2020-07-13'  # 回测结束时间
universe = DynamicUniverse('HS300')  # 证券池，支持股票、基金、期货、指数四种资产
# universe = set_universe('SH50')
# universe = ['601012.XSHG']
benchmark = 'HS300'  # 策略参考标准
freq = 'd'  # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1  # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

max_history_window = 60  # 设置最长回测周期

# 配置账户信息，支持多资产多账户
accounts = {
    'fantasy_account': AccountConfig(account_type='security', capital_base=1500000)
}

# manager = Manager(PEChecker(), MindlessTrader('fantasy_account'))
manager = Manager([DCChecker()], TurtleTrader('fantasy_account', 0.01, 5))


def initialize(context):
    pass


def handle_data(context):
    manager.daily(context)
