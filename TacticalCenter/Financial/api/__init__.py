import datetime as dt
import akshare as ak
import execjs
import requests
import json
import pandas as pd
import os
import tushare as ts


class WenCai:
    def __init__(self):
        module_path = os.path.dirname(__file__)

        with open(module_path + '/xuangu.js', 'r') as f:
            js_content = f.read()
        self.context = execjs.compile(js_content)

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            'Cookie': "",
            "Host": "www.iwencai.com",
            "Referer": "http://www.iwencai.com/stockpick?tid=stockpick",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }

        self.base_url = 'http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data?&secondary_intent=stock&perpage=500&page=1&block_list=&token=c0a8d1d315985718214337154&source=Ths_iwencai_Xuangu&version=2.0&question='

    def query_with(self, question: str = '20211213连板，非ST') -> pd.DataFrame:
        url = self.base_url + question
        self.headers['cookie'] = 'v={}'.format(self.context.call("v"))

        res = requests.get(headers=self.headers, url=url)
        info = json.loads(res.text)
        result_list = info['data']['answer'][0]["txt"][0]["content"]["components"][0]["data"]["datas"]

        df = pd.DataFrame(result_list)
        return df


class TuShare:
    def __init__(self):
        ts.set_token(os.getenv('TUSHARE_TOKEN'))
        self.pro = ts.pro_api()

    def trade_days_from_to(self, from_day='20211101', to_day='20211208') -> list:
        df = self.pro.query('trade_cal', start_date=from_day, end_date=to_day)
        wanted_days = df[df.is_open == 1].cal_date.to_list()
        return wanted_days

    def trade_days(self, start_date='20180101', duration=10) -> list:
        from datetime import datetime
        # 构建
        now = datetime.now().strftime('%Y%m%d')
        df = self.pro.query('trade_cal', start_date=start_date, end_date=now)
        wanted_days = df[df.is_open == 1][0:duration].cal_date.to_list()
        return wanted_days

    def daily(self, ts_code: str, start_date: str, end_date: str):
        """
        获取行情数据
        :param start_date
        :param end_date
        :return: https://tushare.pro/document/2?doc_id=27
        """
        bars: pd.DataFrame = self.pro.daily(ts_code=ts_code, start_date=start_date,
                                            end_date=end_date)
        bars.set_index(['ts_code', 'trade_date'], inplace=True)
        return bars


class AkShare:
    def __init__(self):
        self.name = 'akshare'

    def trade_calendar(self):
        return ak.tool_trade_date_hist_sina()





if __name__ == '__main__':
    # print(WenCai().query_with('20211104连板，非ST，非新股，20211105首次涨停时间'))
    # ts = TuShare()
    # print(ts.trade_days_from_to(from_day='20220112', to_day='20220216'))
    # print(ts.trade_days())
    print(AkShare().trade_calendar())
