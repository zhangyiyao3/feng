from datetime import datetime
from typing import List
from czsc.data.jq import get_kline, get_index_stocks
import czsc
from czsc.analyze import CZSC
from czsc.enum import Signals
# 如果需要实盘行情，导入聚宽数据
from czsc.data.jq import *

assert czsc.__version__ == '0.6.10'

def is_buy(symbol):
    """判断一个股票现在是否有日线一买"""
    bars = get_kline(symbol, freq="D", end_date=datetime.now(), count=1000)
    c = CZSC(bars, freq="日线")
    signals=[]

    # 在这里判断是否有买入形态
    if c.signals['倒1九笔'] in [Signals.X9LA0.value]:
        signals.append('一买')
    if c.signals['倒2九笔'] in [Signals.X9LA0.value]:
        signals.append('二买')
    if c.signals['倒1五笔'] in [Signals.X5LB0.value, Signals.X5LB1.value]:
        signals.append('三买')
    return signals


if __name__ == '__main__':
    # 获取上证50最新成分股列表，这里可以换成自己的股票池
    # symbols: List = get_index_stocks("000016.XSHG")
    symbols: List = get_all_securities()
    for symbol in symbols:
        # print("聚宽剩余调用次数：{}".format(get_query_count()))
        try:
            signals=is_1buy(symbol)
            if len(signals)>0:
                print("{} - {}".format(symbol,signals))
        except:
            print("{} - 执行失败".format(symbol))
