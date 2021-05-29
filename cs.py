from datetime import datetime
from typing import List
from czsc.data.jq import get_kline, get_index_stocks
import czsc
from czsc.analyze import CZSC, RawBar
from czsc.enum import Signals
# 如果需要实盘行情，导入聚宽数据
from czsc.data.jq import *
import traceback
import baostock as bs
import pandas as pd
import tushare as ts

assert czsc.__version__ == '0.6.10'


def bstock():
    bs.login()
    # 获取指定日期的指数、股票列表信息
    end_date = datetime.now()
    e_date = end_date - timedelta(days=10)
    start_date = end_date - timedelta(days=1000)
    start_date, end_date = datetime.strftime(start_date, '%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    stock_rs = bs.query_all_stock(e_date.strftime('%Y-%m-%d'))
    stock_df = stock_rs.get_data()
    # print(stock_df["code"])
    #针对股票列表，逐个处理：获取历史数据生成dataframe、格式化、传入
    bars = []
    for symbol in ["sh.600610",'sh.600614']:
        try:
            data_df = pd.DataFrame()
            k_rs = bs.query_history_k_data_plus(symbol,"date,code,open,high,low,close,volume", start_date, end_date)
            data_df = data_df.append(k_rs.get_data())
            print("{} - {}".format(symbol,data_df))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))
        finally:
            bars.clear()
    bs.logout()


if __name__ == '__main__':
    # tshare()
    # jquan()
    bstock()