import datetime as dt
import akshare as ak
import execjs
import requests
import json
import pandas as pd


class WenCai:
    def __init__(self):
        with open('./xuangu.js', 'r') as f:
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


if __name__ == '__main__':
    print(WenCai().query_with('昨日连板，今日竞价涨幅>8%'))
