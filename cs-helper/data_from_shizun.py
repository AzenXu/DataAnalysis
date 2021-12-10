# content = '''
# 1、指数：大盘+1.07%，创业板：+2.46%
# 情绪：分歧  日内主线：稀土，新能源汽车，业绩预增
# 2、涨停统计：
# 涨停板：78只，跌停板：4只
# 连板25只，首板：53只
# 炸板29只，炸板率：27.1%
# 3、晋级率：
# 首板晋级率：26.3%
# 连板晋级率：55.5%
# 晋级成功率：较好
# 4、连板晋级失败：
# 当天平均盈亏：-6.28%
# 隔日平均开盘：-1.40%
# 当天打板失败平均亏损：-3.66%
# 隔日平均开盘：-2.21%
# '''

content = '''
1、指数：大盘-0.36%，创业板：-1.27%  
情绪：上升 日内主线：上海本地股  ST摘帽
2、涨停统计：
涨停板：63只 跌停板：7只
连板14只，首板：49只
炸板30只，炸板率：32.3%
3、晋级率：
首板晋级率：25.6%
连板晋级率：26.7%
晋级成功率：一般
4、连板晋级失败：
当天平均盈亏：-1.17%
隔日平均开盘：-2.00%
当天打板失败平均亏损：-3.85%
隔日平均开盘：-1.54%
'''

import re


def data_pickup(txt: str):
    print(txt)

    # pattern = re.compile(r'\d+')  # 查找数字
    # result1 = pattern.findall('runoob 123 google 456')
    # result2 = pattern.findall('run88oob123google456', 0, 10)
    #
    # print(result1[0])
    # print(result2)

    indexObj = re.search('1、指数：大盘(.*%)，[\n.]*创业板：(.*%) {2}', txt)
    indexObj2 = re.search('涨停板：(\d*)只 跌停板：(\d*)只', txt)
    indexObj3 = re.search('连板\D*(\d*)只，首板\D*(\d*)只', txt)
    indexObj4 = re.search('炸板\D*(\d*)只，炸板率\D*(\d.*%)', txt)
    indexObj5 = re.search(
        '首板晋级率\D*(\d[^%]*%)\n连板晋级率\D*(\d[^%]*%)[^当]*当天平均盈亏：([^%]*%)[^隔]*隔日平均开盘：([^%]*%)[^当]*当天打板失败平均亏损：([^%]*%)[^隔]*隔日平均开盘：([^%]*%)',
        txt, re.DOTALL)

    if indexObj:
        print(indexObj.groups(), indexObj2.groups(), indexObj3.groups(), indexObj4.groups(), indexObj5.groups())
        print(indexObj.group(1), indexObj.group(2), indexObj2.group(1), indexObj2.group(2), indexObj3.group(1),
              indexObj3.group(2), indexObj4.group(1), indexObj4.group(2), indexObj5.group(1), indexObj5.group(2),
              indexObj5.group(3), indexObj5.group(4), indexObj5.group(5), indexObj5.group(6))

    # groupObj = re.search('涨停板：(\d*)只，跌停板：(\d*)只.*连板：(\d*)只', txt)

    # if groupObj:
    #     print("searchObj.group(1) : ", groupObj.group(1))
    #     print("searchObj.group(2) : ", groupObj.group(2))


if __name__ == '__main__':
    data_pickup(content)
