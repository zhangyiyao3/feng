from datetime import datetime
import os
import struct
import traceback
from typing import List

from czsc.objects import RawBar
import pandas as pd

TDX_DIR = r"D:\new_tdxqh"  # 首先要设置通达信的安装目录


def tdx():
    # 找出沪市6开头的，中三买的票
    rootdir = TDX_DIR + r"\vipdoc\sh\lday"
    signals_list = []  #用来存储所有证券的信号，一只证券可能存在多个信号
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        try:
            symbol = list[i][2:8]
            # if symbol.startswith("6000"):
            bars = get_data_from_tdxfile(symbol, 'sh')
            # signals = is_buy(bars)
            if len(signals) > 0:  #若存在信号，把证券及其信号，存入signals_list
                signals_list.append({symbol + '.sh': signals})
                print("{}{} - {}".format('sh', symbol, signals))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))

    # 找出深圳中0开头的三买的票
    rootdir = TDX_DIR + r"\vipdoc\sz\lday"
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        try:
            symbol = list[i][2:8]
            # if symbol.startswith("00000"):
            bars = get_data_from_tdxfile(symbol, 'sz')
            # signals = is_buy(bars)
            if len(signals) > 0:
                signals_list.append({symbol + '.sz': signals})
                print("{}{} - {}".format('sz', symbol, signals))
        except Exception as e:
            traceback.print_exc()
            print("{} 执行失败 - {}".format(symbol, e))


# 从通达信目录读入数据
def get_data_from_tdxfile(stock_code, type) -> List[RawBar]:
    '''
    stock_code:股票代码 600667
    type：市场代码，sh沪市，sz深市
    '''
    bars = []
    filepath = TDX_DIR + r'\vipdoc\\' + type + r'\lday\\' + type + stock_code + '.day'
    with open(filepath, 'rb') as f:
        while True:
            stock_date = f.read(4)
            stock_open = f.read(4)
            stock_high = f.read(4)
            stock_low = f.read(4)
            stock_close = f.read(4)
            stock_amount = f.read(4)
            stock_vol = f.read(4)
            stock_reservation = f.read(4)
            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)  # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)  # 开盘价*100
            stock_high = struct.unpack("l", stock_high)  # 最高价*100
            stock_low = struct.unpack("l", stock_low)  # 最低价*100
            stock_close = struct.unpack("l", stock_close)  # 收盘价*100
            stock_amount = struct.unpack("f", stock_amount)  # 成交额
            stock_vol = struct.unpack("l", stock_vol)  # 成交量
            stock_reservation = struct.unpack("l", stock_reservation)  # 保留值
            date_format = datetime.strptime(str(stock_date[0]),
                                            '%Y%M%d')  # 格式化日期
            date_format = date_format.strftime('%Y-%M-%d')

            bar = RawBar(symbol=stock_code,
                         dt=pd.to_datetime(date_format),
                         open=stock_open[0] / 100,
                         close=stock_close[0] / 100.0,
                         high=stock_high[0] / 100.0,
                         low=stock_low[0] / 100.0,
                         vol=stock_vol[0])
            bars.append(bar)
        return bars


# 使用第三方数据，只需要定义一个K线转换函数
def format_kline(symbol,kline: pd.DataFrame) -> List[RawBar]:
    """
    :param kline: Tushare 数据接口返回的K线数据
    :return: 转换好的K线数据
    """
    bars = []
    records = kline.to_dict('records')
    for record in records:
        # 将每一根K线转换成 RawBar 对象
        bar = RawBar(symbol=symbol,
                     dt=pd.to_datetime(record['datetime']),
                     open=record['open'],
                     close=record['close'],
                     high=record['high'],
                     low=record['low'],
                     vol=record['vol'])
        bars.append(bar)
    return bars