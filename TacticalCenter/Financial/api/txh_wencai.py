import execjs
import requests
import json
import pandas as pd

with open('./xuangu.js', 'r') as f:
    jscontent = f.read()
context = execjs.compile(jscontent)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    'Cookie': "",
    "Host": "www.iwencai.com",
    "Referer": "http://www.iwencai.com/stockpick?tid=stockpick",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}


def query_with(question='20211213连板，非ST') -> pd.DataFrame:
    url = 'http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data?&secondary_intent=stock&perpage=500&page=1&block_list=&token=c0a8d1d315985718214337154&source=Ths_iwencai_Xuangu&version=2.0&question='
    url = url + question
    headers['cookie'] = 'v={}'.format(context.call("v"))
    res = requests.get(headers=headers, url=url)
    info = json.loads(res.text)
    result_list = info['data']['answer'][0]["txt"][0]["content"]["components"][0]["data"]["datas"]
    print(len(result_list))
    df = pd.DataFrame(result_list)

    return df


if __name__ == '__main__':
    query_with()
