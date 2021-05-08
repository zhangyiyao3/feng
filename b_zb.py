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

# 使用第三方数据，只需要定义一个K线转换函数
def format_kline_ts(kline: pd.DataFrame) -> List[RawBar]:
    """
    :param kline: Tushare 数据接口返回的K线数据
    :return: 转换好的K线数据
    """
    bars = []
    records = kline.to_dict('records')
    for record in records:
        # 将每一根K线转换成 RawBar 对象
        bar = RawBar(symbol=record['ts_code'], dt=pd.to_datetime(record['trade_date']), open=record['open'],
                     close=record['close'], high=record['high'], low=record['low'], vol=record['vol'])
        bars.append(bar)
    return bars

# 使用第三方数据，只需要定义一个K线转换函数
def format_kline_bs(kline: pd.DataFrame) -> List[RawBar]:
    """
    :param kline: Tushare 数据接口返回的K线数据
    :return: 转换好的K线数据
    """
    bars = []
    records = kline.to_dict('records')
    for record in records:
        # 将每一根K线转换成 RawBar 对象
        bar = RawBar(symbol=record['ts_code'], dt=pd.to_datetime(record['trade_date']), open=record['open'],
                     close=record['close'], high=record['high'], low=record['low'], vol=record['vol'])
        bars.append(bar)
    return bars

def is_buy(bars:List[RawBar]) -> List:
    """判断一个股票现在是否有买入信号，没有则返回[]"""
    c = CZSC(bars, freq="日线")
    signals=[]
    # 在这里判断是否有买入形态
    if c.signals['倒1九笔'] in [Signals.X9LA0.value]:
        signals.append('一买')
    if c.signals['倒2九笔'] in [Signals.X9LA0.value]:
        signals.append('二买')
    if c.signals['倒1五笔'] in [Signals.X5LB0.value]:
        signals.append('三买')
    return signals

def tshare():
    # 获取上证50最新成分股列表，这里可以换成自己的股票池
    symbols: List = ["000985.SH"]
    # symbols: List = get_index_stocks("000985.XSHG")
    for symbol in symbols:
        try:
            # 调用tushare的K线获取方法，Tushare数据的使用方法，请参考：https://tushare.pro/document/2
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1000)
            df = ts.pro_bar(ts_code=symbol, adj='qfq', asset="E",
                            start_date=start_date.strftime("%Y%m%d"),
                            end_date=end_date.strftime("%Y%m%d"))
            bars = format_kline_ts(df)
            signals=is_buy(bars)
            if len(signals)>0:
                print("{} - {}".format(symbol,signals))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))


def jquan():
    # 获取上证50最新成分股列表，这里可以换成自己的股票池
    symbols: List = ["000985.XSHG"]
    # symbols: List = get_index_stocks("000985.XSHG")
    for symbol in symbols:
        try:
            bars = get_kline(symbol, freq="D", end_date=datetime.now(), count=1000)
            signals=is_buy(bars)
            if len(signals)>0:
                print("{} - {}".format(symbol,signals))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))
    print("聚宽剩余调用次数：{}".format(get_query_count()))

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
    # for symbol in ["sh.000001",'sh.000002']:
    for symbol in stock_df["code"]:
        data_df = pd.DataFrame()
        k_rs = bs.query_history_k_data_plus(symbol,"date,code,open,high,low,close,volume", start_date, end_date)
        data_df = data_df.append(k_rs.get_data())
        #格式化bars
        bars = []
        records = data_df.to_dict('records')
        for record in records:
            # 将每一根K线转换成 RawBar 对象
            bar = RawBar(symbol=record['code'], dt=pd.to_datetime(record['date']), open=float(record['open']),
                        close=float(record['close']), high=float(record['high']), low=float(record['low']), vol=float(record['volume']))
            bars.append(bar)
        try:
            signals=is_buy(bars)
            if len(signals)>0:
                print("{} - {}".format(symbol,signals))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))
    bs.logout()

def bb():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取中证500成分股
    rs = bs.query_zz500_stocks()
    print('query_zz500 error_code:'+rs.error_code)
    print('query_zz500  error_msg:'+rs.error_msg)

    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv("D:/zz500_stocks.csv", encoding="gbk", index=False)
    print(result)

    # 登出系统
    bs.logout()

def download_data():
    bs.login()
    # 获取指定日期的指数、股票数据
    stock_rs = bs.query_all_stock()
    stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1000)
    start_date, end_date=datetime.strftime(start_date,'%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    for code in ["sh.600000"]:
    # for code in stock_df["code"]:
        k_rs = bs.query_history_k_data_plus(code,"date,code,open,high,low,close,volume", start_date, end_date)
        data_df = data_df.append(k_rs.get_data())
    bars = []
    records = data_df.to_dict('records')
    for record in records:
        # 将每一根K线转换成 RawBar 对象
        bar = RawBar(symbol=record['code'], dt=pd.to_datetime(record['date']), open=record['open'],
                     close=record['close'], high=record['high'], low=record['low'], vol=record['volume'])
        bars.append(bar)
    bs.logout()
    print(bars)

if __name__ == '__main__':
    # tshare()
    # jquan()
    bstock()
    # bb()
    # download_data()
"""     first = []
    last = []
    lists_more = [1, 2, 3, 4, 5, 6]

    for i in lists_more:
        first.append(i)
        last.append(first)
        print('before',first)
        first = []
        print('after',first)
    print(first) """

