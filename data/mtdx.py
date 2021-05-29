# -*- coding: utf-8 -*-
from mootdx.quotes import Quotes
from mootdx.affair import Affair


def fin():
    # 远程文件列表
    files = Affair.files()
    print(files)

    # 下载单个
    # Affair.fetch(downdir='tmp', filename='gpcw19960630.zip')

    # # 下载全部
    # Affair.parse(downdir='tmp')

def quote():
    client = Quotes.factory(market='std')  # 标准市场
    # client = Quotes.factory(market='ext', multithread=True, heartbeat=True) # 扩展市场

    quote = client.bars(symbol='600036', frequency=7, offset=800)
    print(quote)
    # quote = client.bars(symbol='600036', frequency=8, offset=10)
    # print(quote)
    quote = client.index(symbol='000001', frequency=9)
    print(quote)

    quote = client.minute(symbol='000001')
    print(quote)

if __name__ == '__main__':
    quote()
