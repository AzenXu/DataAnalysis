import tushare as ts
import os

ts.set_token(os.getenv('TUSHARE_TOKEN'))
pro = ts.pro_api()
df = pro.daily(ts_code='002230.sz', start_date='1900-01-01', end_date='2099-01-01')
print(df)