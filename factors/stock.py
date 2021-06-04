from collections import OrderedDict
from data.ptdx import get_finance_overview
from czsc.enum import Signals

stock_factors = [
    '二级行业', '总市值/亿', 'ROE%', 'ROA%', '毛利率%', '净利率%', '毛利增长率%', '收入增长率%',
    '资产负债率%', '营业收入/亿', 'PEG', '动PE', '静PE', 'PB', 'PS', '现金流/净利润', '经营cash/亿',
    '总cash/亿'
]

tec_factors = [
    'ma由高至低(含股价)', '向上ma', '向下ma', '信号至今涨跌%', '信号至今日均涨跌%', '20抵扣价5D方向',
    '60抵扣价5D方向', '120抵扣价5D方向', '250抵扣价5D方向'
]


def get_finance_factors(market, symbol, cur_price):
    '''财务因子，使用pytdx作为数据源'''
    s = OrderedDict({})

    #财务数据概况
    fo = get_finance_overview(market, symbol)
    s['二级行业'] = fo['industry']
    s['总市值'] = fo['zongguben'] * cur_price / 100000000
    s['ROE'] = fo['jinglirun'] / fo['jingzichan'] * 100
    s['ROA'] = fo['jinglirun'] / fo['zongzichan'] * 100
    s['净利率'] = fo['jinglirun'] / fo['zhuyingshouru'] * 100
    s['毛利率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
    # s['毛利增长率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
    # s['收入增长率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
    s['资产负债率'] = (fo['zongzichan'] - fo['jingzichan']) / fo['zongzichan'] * 100
    s['营业收入'] = fo['zhuyingshouru']
    s['PE'] = cur_price / (fo['jinglirun'] / fo['zongguben'])
    # s['PEG'] = s['PE'] / s['毛利增长率']
    s['PB'] = cur_price / fo['meigujingzichan']
    s['PS'] = cur_price / (fo['zhuyingshouru'] / fo['zongguben'])
    s['现金流/净利润'] = fo['jingyingxianjinliu'] / fo['jinglirun']
    s['经营cash'] = fo['jingyingxianjinliu'] / 100000000
    s['总现金cash'] = fo['zongxianjinliu'] / 100000000
    return s


def get_tec_factors(market, symbol):
    '''技术因子'''
    s = OrderedDict({})

    #财务数据概况
    fo = get_finance_overview(market, symbol)
    s['行业'] = fo['industry']
    s['总市值'] = fo['zongguben'] * close / 100000000
    s['经营cash'] = fo['jingyingxianjinliu'] / 100000000
    s['总现金cash'] = fo['zongxianjinliu'] / 100000000
    s['ROE'] = fo['jinglirun'] / fo['jingzichan'] * 100
    s['净利率'] = fo['jinglirun'] / fo['zhuyingshouru'] * 100
    s['毛利率'] = fo['yingyelirun'] / fo['zhuyingshouru'] * 100
    s['资产负债率'] = (fo['zongzichan'] - fo['jingzichan']) / fo['zongzichan'] * 100
    s['PE'] = close / (fo['jinglirun'] / fo['zongguben'])
    s['PB'] = close / fo['meigujingzichan']
    # s['ma5'] = ''
    # s['信号价格'] = ''
    # s['信号出现后涨跌幅'] = 0
    return s


if __name__ == '__main__':
    print(get_finance_factors('sz', '000001', 5))
