# coding: utf-8

import sys
sys.path.insert(0, ".")
sys.path.insert(0, "..")

import datetime

print(datetime.date(2200, 1, 1))

import czsc
print(czsc.__version__)
assert czsc.__version__ >= "0.6.1"

from czsc.analyze import CZSC
from czsc.trader import CzscTrader


# 如果需要实盘行情，导入聚宽数据
from czsc.data.jq import *

# 首次使用需要设置聚宽账户
# set_token("18678788767", '000111') # 第一个参数是JQData的手机号，第二个参数是登录密码
print("聚宽剩余调用次数：{}".format(get_query_count()))

ct = CzscTrader(symbol="300803.XSHE", max_count=1000, end_date=datetime.now())
# max_count 参数控制获取的K线数量
# end_date  参数控制获取K线的截止时间，便于查看历史分析结果，默认为当下时间

# 可视化分析结果
# chart = ct.kf.take_snapshot(width="900px", height="480px")
# chart.render_notebook()
ct.open_in_browser(width="1400px", height="580px")

# 调用选股方法判断是否有满足的选股条件
# ct.run_selector()
print(ct.run_selector())
print('hi')

