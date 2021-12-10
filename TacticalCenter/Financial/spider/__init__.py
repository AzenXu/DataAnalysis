import bs4 as bs
import requests  # python的http客户端
import pickle  # 用于序列化反序列化

import datetime as dt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
import matplotlib.pyplot as plt
import os


def GetHuStock():
    """
    爬取所有股票名 + Code到本地，文件名：huStock.pickle
    :return:
    """
    res = requests.get('https://www.banban.cn/gupiao/list_sh.html')
    # 防止中文乱码
    res.encoding = res.apparent_encoding
    # 使用bsoup的lxml样式
    soup = bs.BeautifulSoup(res.text, 'lxml')
    # 从html内容中找到类名为'u-postcontent cz'的div标签
    content = soup.find('div', {'class': 'u-postcontent cz'})
    result = []
    for item in content.findAll('a'):
        result.append(item.text)
    with open('huStock.pickle', 'wb') as f:
        pickle.dump(result, f)


def GetStockFromYahoo(isHaveStockCode=False):
    if not isHaveStockCode:
        GetHuStock()
    with open('huStock.pickle', 'rb') as f:
        tickets = pickle.load(f, encoding='gb2312')
    if not os.path.exists('StockDir'):
        os.makedirs('StockDir')

    for ticket in tickets:
        arr = ticket.split('(')
        stock_name = arr[0]
        stock_code = arr[1][:-1] + '.ss'
        if os.path.exists('StockDir/{}.csv'.format(stock_name + stock_code)):
            print('已下载')
        else:
            DownloadStock(stock_name, stock_code)
            print('下载{}中...'.format(stock_name))


def DownloadStock(stockName, stockCode):
    style.use('ggplot')
    start = dt.datetime(2014, 1, 1)
    end = dt.datetime(2020, 7, 31)
    # 根据股票代码从雅虎财经读取该股票在制定时间段的股票数据
    df = web.DataReader(stockCode, 'yahoo', start, end)
    # 保存为对应的文件
    df.to_csv('StockDir/{}.csv'.format(stockName + stockCode))


if __name__ == '__main__':
    print('spider comes here')
    # GetHuStock()

    GetStockFromYahoo()
