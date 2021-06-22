from collections import OrderedDict

from czsc.analyze import CZSC
import pandas as pd
from data.ptdx import get_finance_overview
from czsc.enum import Signals
import numpy as np
import talib
import traceback

stock_factors = [
    '二级行业', '地域', '总市值/亿', 'ROE%', 'ROA%', '毛利率%', '净利率%', '毛利增长率%', '收入增长率%',
    '资产负债率%', '营业收入/亿', 'PEG', '动PE', '静PE', 'PB', 'PS', '现金流/净利润', '经营cash/亿',
    '总cash/亿'
]

tec_factors = [
    'ma由高至低(含股价)', '向上ma', '向下ma', '信号至今涨跌%', '信号至今日均涨跌%', '20抵扣价5D方向',
    '60抵扣价5D方向', '120抵扣价5D方向', '250抵扣价5D方向'
]


def get_finance_factors(market, symbol, czsc: CZSC):
    '''财务因子，使用pytdx作为数据源'''
    s = OrderedDict({})

    #财务数据概况
    fo = get_finance_overview(market, symbol)
    # print(fo)
    if fo['industry'] != 0:  #若无行业数据，说明不是股票，不再计算财务因子
        cur_price = czsc.bars_raw[-1].close
        s['二级行业'] = fo['industry']
        s['地域'] = fo['province']
        s['总市值'] = fo['zongguben'] * cur_price / 100000000
        s['ROE'] = fo['jinglirun'] / fo['jingzichan'] * 100
        s['ROA'] = fo['jinglirun'] / fo['zongzichan'] * 100
        s['净利率'] = fo['jinglirun'] / fo['zhuyingshouru'] * 100
        s['毛利率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
        # s['毛利增长率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
        # s['收入增长率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
        s['资产负债率'] = (fo['zongzichan'] -
                      fo['jingzichan']) / fo['zongzichan'] * 100
        s['营业收入'] = fo['zhuyingshouru'] / 100000000
        s['PE'] = cur_price / (fo['jinglirun'] / fo['zongguben'])
        # s['PEG'] = round(s['PE'] / s['毛利增长率']
        s['PB'] = cur_price / (fo['jingzichan'] / fo['zongguben'])
        s['PS'] = cur_price / (fo['zhuyingshouru'] / fo['zongguben'])
        s['现金流/净利润'] = fo['jingyingxianjinliu'] / fo['jinglirun']
        s['经营cash'] = fo['jingyingxianjinliu'] / 100000000
        s['总现金cash'] = fo['zongxianjinliu'] / 100000000
    return s


def get_tec_factors(czsc: CZSC):
    '''技术因子'''
    s = OrderedDict({})

    s['ubil'] = czsc.signals['未完成笔长度'] - 1
    close = czsc.close
    ma5 = talib.MA(close, timeperiod=5)
    ma10 = talib.MA(close, timeperiod=10)
    ma20 = talib.MA(close, timeperiod=20)
    ma60 = talib.MA(close, timeperiod=60)
    ma120 = talib.MA(close, timeperiod=120)
    ma250 = talib.MA(close, timeperiod=250)
    # print(czsc.symbol, close.size)
    # print(close,ma5)
    df = pd.DataFrame({
        '5': ma5[-2:],
        '10': ma10[-2:],
        '20': ma20[-2:],
        '60': ma60[-2:],
        '120': ma120[-2:],
        '250': ma250[-2:],
        'c': close[-2:]
    })
    s['ma由高至低(含股价)'] = df.sort_values(axis=1, by=1,
                                      ascending=False).columns.tolist()
    s['向上ma'] = df.columns[df.iloc[1] > df.iloc[0]].tolist()
    s['向下ma'] = df.columns[df.iloc[1] < df.iloc[0]].tolist()
    s['走平ma'] = df.columns[df.iloc[1] == df.iloc[0]].tolist()
    n = 5  #未来N天抵扣价与当前价的对比
    try:
        s['5抵扣价5D'] = '多' if close[-5] < close[-1] else '空'
        s['10抵扣价5D'] = '多' if close[-10 + n] < close[-1] else '空'
        s['20抵扣价5D'] = '多' if close[-20 + n] < close[-1] else '空'
        s['60抵扣价5D'] = '多' if close[-60 + n] < close[-1] else '空'
        s['120抵扣价5D'] = '多' if close[-120 + n] < close[-1] else '空'
        s['250抵扣价5D'] = '多' if close[-250 + n] < close[-1] else '空'
    except Exception as e:
        traceback.print_exc()
        print('次新股，均线尚未全部形成')
    cur_price = czsc.bars_raw[-1].close
    fx_price = czsc.bi_list[-1].fx_b.fx
    s['信号至今涨跌%'] = (cur_price - fx_price) / fx_price * 100
    s['信号至今单Bar涨跌%'] = s['信号至今涨跌%'] / s['ubil']
    return s


if __name__ == '__main__':
    print(get_finance_factors('sh', '600012', 5))
