from collections import OrderedDict
from pytdx.hq import TdxHq_API
# from . import base

ip = '119.147.212.81'
port = 7709

api = TdxHq_API()

market_map = {
    0: 'sz',
    1: 'sh',
}

market_inv = {v: k for k, v in market_map.items()}


def get_finance_overview(market, symbol) -> OrderedDict:
    with api.connect(ip, port):
        # slist=api.get_security_list(1, 0)
        finance_info = api.get_finance_info(market_inv[market], symbol)
    return finance_info


if __name__ == '__main__':
    print(get_finance_overview('sz', '000001'))
