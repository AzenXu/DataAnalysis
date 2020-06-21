class Stock:
    def __init__(self, code, name, asset='E'):
        self.code = code
        self.asset = asset
        self.name = name


xunfei = Stock(code='002230.sz', name='科大讯飞')
mengjie = Stock(code='002397.sz', name='梦洁家纺')  # AQF - Aberration系统用到的DemoStock
hs300 = Stock(code='000300.sh', name='沪深300', asset='I')

