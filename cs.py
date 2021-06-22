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
from pytdx.hq import TdxHq_API
from mootdx.quotes import Quotes
from mootdx import consts
# import QUANTAXIS as QA
from mootdx.affair import Affair

assert czsc.__version__ == '0.7.2'


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


def ptdx():
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        df=api.to_df(api.get_security_list(1, 10000))
        print(df)


def mtdx():
    client = Quotes.factory(market='std')
    symbol = client.stocks(market=consts.MARKET_SH)
    print(symbol)

def qa():
    QA.QA_util_log_info('日线数据')
    QA.QA_util_log_info('不复权')
    data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('000001','2017-01-01','2017-01-31')
    print(data)
    print(QA.QA_fetch_stock_block_adv('000001'))
    res = QA.QA_fetch_financial_report(
        ['000001', '600100'],
        ['2017-03-31', '2017-06-30', '2018-12-31', '2019-12-31', '2020-12-31'])
    print(res)
    res_adv=QA.QA_fetch_financial_report_adv('600000','2017-01-01','2018-05-01')
    print(res_adv.data)
    fds=QA.QA_DataStruct_Financial(res)
    print(fds.get_key('600100', '2020-12-31', 'ROE'))
    print(fds.get_report_by_date('600100', '2020-12-31'))


from mootdx.reader import Reader


def mtdx_fin():
    print(Affair.files())
    Affair.fetch(downdir='output', filename='gpcw20210331.zip')
    data = Affair.parse(downdir='output', filename='gpcw20210331.zip')
    result = Affair.parse(downdir='output', filename='gpcw20210331.zip')
    result.to_csv('gpcw20210331.csv')

def mtdx_blk():
    reader = Reader.factory(market='std', tdxdir=r"D:\new_tdxqh")
    # 分组格式
    print(reader.block(symbol='block_zs', group=True))
    print(reader.block(symbol='incon', group=True))


if __name__ == '__main__':
    # tshare()
    # jquan()
    # bstock()
    # ptdx()
    # mtdx()
    # qa()
    mtdx_blk()
